import os
from unittest import TestCase

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import to_hex  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402

from sport_activities_features import HillIdentification, TCXFile  # noqa: E402
from sport_activities_features.plot_data import (  # noqa: E402
    HILL_GRADE_COLORS,
    PlotData,
)


def fill_colors(ax):
    """Face colours of all filled areas on the axes."""
    colors = set()
    for collection in ax.collections:
        for color in collection.get_facecolor():
            colors.add(to_hex(color))
    return colors


def texts(ax):
    return [text.get_text() for text in ax.texts]


class TestPlotHillsOnMap(TestCase):
    def tearDown(self):
        plt.close('all')

    def plot(self, altitudes, distances, hills, **kwargs):
        fig = PlotData().plot_hills_on_map(
            altitudes, distances, hills, **kwargs,
        )
        return fig, fig.axes[0]

    def test_activity(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', '15.tcx')
        tcx_file = TCXFile()
        activity = tcx_file.extract_activity_data(
            tcx_file.read_one_file(filename),
        )
        hill = HillIdentification(
            activity['altitudes'], activity['distances'], ascent_threshold=30,
        )
        hill.identify_hills()

        fig, ax = self.plot(
            activity['altitudes'], activity['distances'], hill.return_hills(),
        )

        self.assertIsInstance(fig, Figure)
        labels = texts(ax)
        for number in range(1, 8):
            self.assertIn(str(number), labels)
        self.assertIn('+332 m\n7.5 km · 4.4 %', labels)
        self.assertIn(
            '7 hills  ·  1,188 m climbed in hills  ·  1,404 m total ascent',
            labels,
        )
        self.assertEqual(ax.get_xlabel(), 'Distance (km)')
        self.assertAlmostEqual(ax.get_xlim()[1], 116.367, places=2)

    def test_hills_are_coloured_by_grade(self):
        # 1 km at 5 % (class 3–6 %) followed by 1 km at 10 % (class 9–12 %).
        distances = list(range(0, 2001, 10))
        altitudes = [
            d * 0.05 if d <= 1000 else 50 + (d - 1000) * 0.10
            for d in distances
        ]
        _, ax = self.plot(altitudes, distances, [[0, len(distances) - 1]])

        colors = fill_colors(ax)
        self.assertIn(HILL_GRADE_COLORS[1], colors)
        self.assertIn(HILL_GRADE_COLORS[3], colors)
        self.assertNotIn(HILL_GRADE_COLORS[0], colors)
        self.assertNotIn(HILL_GRADE_COLORS[2], colors)
        self.assertNotIn(HILL_GRADE_COLORS[4], colors)
        self.assertIn('+150 m\n2.0 km · 7.5 %', texts(ax))

    def test_accepts_stored_segments(self):
        hill = HillIdentification([0, 40, 0], [0, 400, 800])
        hill.identify_hills()
        _, ax = self.plot([0, 40, 0], [0, 400, 800], hill.identified_hills)
        self.assertIn('+40 m\n0.4 km · 10.0 %', texts(ax))

    def test_no_hills(self):
        _, ax = self.plot([10, 12, 11, 15], [0, 100, 200, 300], [])
        labels = texts(ax)
        self.assertEqual(labels, ['No hills identified  ·  6 m total ascent'])
        self.assertEqual(fill_colors(ax) & set(HILL_GRADE_COLORS), set())

    def test_many_hills_show_only_numbers(self):
        altitudes = [0, 40] * 12 + [0]
        distances = [i * 400 for i in range(len(altitudes))]
        hills = [[i, i + 1] for i in range(0, 24, 2)]
        _, ax = self.plot(altitudes, distances, hills)
        labels = texts(ax)
        self.assertEqual(
            [label for label in labels if label.isdigit()],
            [str(n) for n in range(1, 13)],
        )
        self.assertFalse(any('km ·' in label for label in labels))

    def test_missing_values(self):
        _, ax = self.plot(
            [0, None, 20, 40, 0], [0, 100, None, 300, 400], [[0, 3]],
        )
        self.assertIn('1', texts(ax))

    def test_no_data(self):
        with self.assertRaises(ValueError):
            self.plot([None, None], [None, None], [])

    def test_draws_on_given_axes(self):
        fig, ax = plt.subplots()
        result = PlotData().plot_hills_on_map(
            [0, 40, 0], [0, 400, 800], [[0, 1]], ax=ax, title='My ride',
        )
        self.assertIs(result, fig)
        self.assertEqual(ax.get_title(loc='left'), 'My ride')
