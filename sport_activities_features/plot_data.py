import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.patches import Patch

plt.style.use('seaborn-v0_8-whitegrid')

# Hill profile: grade classes (in %) and their colours. One blue hue from
# light to dark, so steeper reads as darker; the steps are far enough apart
# in lightness to be told apart, also with colour vision deficiencies.
HILL_GRADE_BOUNDS = (3, 6, 9, 12)
HILL_GRADE_COLORS = ('#86b6ef', '#3987e5', '#256abf', '#184f95', '#0d366b')
HILL_GRADE_LABELS = ('< 3 %', '3–6 %', '6–9 %', '9–12 %', '≥ 12 %')
_SURFACE = '#fcfcfb'
_TEXT = '#0b0b0b'
_TEXT_SECONDARY = '#52514e'
_TEXT_MUTED = '#8a8984'
_TERRAIN = '#e7e6e1'
_GRID = '#ebeae6'
# Above this many hills only the hill numbers are printed.
_MAX_DETAILED_LABELS = 10


def _to_float_array(values: list) -> np.ndarray:
    """Convert a list that may contain None to a float array with NaN."""
    return np.array(
        [np.nan if v is None else float(v) for v in values], dtype=float,
    )


def _hill_segment(hill) -> tuple:
    """Return (start, end) of a hill given as [start, end] or as
    StoredSegments."""
    segment = getattr(hill, 'segment', hill)
    return int(segment[0]), int(segment[-1])


def _grade_color(grade: float) -> str:
    """Colour of the grade class that the grade (in %) belongs to."""
    return HILL_GRADE_COLORS[int(np.digitize(grade, HILL_GRADE_BOUNDS))]


class PlotData:

    """Class for plotting the extracted data."""

    def get_positions_of_hills(self, identified_hills: list) -> list:
        """Method for retrieving positions of identified hills.\n
        Args:
            identified_hills (list):
                list of identified hills
        Returns:
            list: list of hills.
        """
        points = []
        for i in range(len(identified_hills)):
            for j in range(len(identified_hills[i])):
                points.append(identified_hills[i][j])
        return points

    def get_positions_of_intervals(self, identified_intervals: list) -> list:
        """Method for retrieving positions of identified intervals.\n
        Args:
            identified_intervals (list):
                list of identified intervals
        Returns:
            list: list of intervals.
        """
        points = []
        for i in range(len(identified_intervals)):
            for j in range(len(identified_intervals[i])):
                points.append(identified_intervals[i][j])
        return points

    def show_hills_on_map(
        self,
        altitude: list,
        distance: list,
        identified_hills: list,
        **kwargs,
    ) -> None:
        """Method for rendering all hills identified in data
        on an elevation profile (see plot_hills_on_map).\n
        Args:
            altitude (list):
                list of altitudes
            distance (list):
                list of distances
            identified_hills (list):
                list of identified hills.
            **kwargs:
                passed to plot_hills_on_map.
        """
        self.plot_hills_on_map(
            altitude, distance, identified_hills, **kwargs,
        )
        plt.show()

    def show_intervals_on_map(
        self,
        timestamp: list,
        distance: list,
        identified_intervals: list,
    ) -> None:
        """Method for rendering all intervals identified in data
        on topographic map plot.\n
        Args:
            timestamp (datetime):
                list of timestamps
            distance (float):
                list of distances
            identified_intervals (list):
                list of identified intervals.
        """
        plt = self.plot_intervals_in_map(timestamp, identified_intervals)
        plt.show()

    def show_basic_map(self) -> None:
        """Method for rendering the whole topographic map plot."""
        plt = self.plot_basic_map()
        plt.show()

    def plot_hills_on_map(
        self,
        altitude: list,
        distance: list,
        identified_hills: list,
        title: str = 'Identified hills',
        segment_length: float = 500,
        ax=None,
    ) -> Figure:
        """Method for plotting identified hills on the elevation profile
        of an activity.\n
        The whole route is drawn as a grey silhouette. Every hill is
        divided into pieces of about segment_length meters, and each piece
        is coloured by its average grade. Each hill is numbered at its
        summit and labelled with its elevation gain, length and average
        grade (only the numbers are shown when there are more than ten
        hills).\n
        Args:
            altitude (list):
                list of altitudes in meters
            distance (list):
                list of cumulative distances in meters
            identified_hills (list):
                identified hills as [start_index, end_index] pairs
                (HillIdentification.return_hills()) or StoredSegments
                (HillIdentification.identified_hills)
            title (str):
                title of the plot
            segment_length (float):
                length in meters of the pieces of a hill that are coloured
                by their grade
            ax (matplotlib.axes.Axes):
                optional axes to draw on; a new figure is created if None
        Returns:
            matplotlib.figure.Figure: figure with the plot; use
            fig.savefig(...) to save it or plt.show() to display it.
        """
        altitudes = _to_float_array(altitude)
        distances = _to_float_array(distance)
        valid = ~np.isnan(altitudes) & ~np.isnan(distances)
        if not valid.any():
            msg = 'No altitude and distance data to plot.'
            raise ValueError(msg)
        hills = [_hill_segment(hill) for hill in identified_hills]
        km = distances / 1000

        if ax is None:
            fig, ax = plt.subplots(figsize=(12, 4.6), dpi=110)
        else:
            fig = ax.figure
        fig.patch.set_facecolor(_SURFACE)
        ax.set_facecolor(_SURFACE)

        lowest = np.nanmin(altitudes[valid])
        highest = np.nanmax(altitudes[valid])
        span = max(highest - lowest, 1.0)
        base = lowest - 0.04 * span

        # Whole route as a quiet silhouette.
        ax.fill_between(km, altitudes, base, color=_TERRAIN, lw=0, zorder=1)
        ax.plot(km, altitudes, color=_TEXT_MUTED, lw=1.0, zorder=3)

        # Hills, piece by piece, coloured by grade.
        for start, end in hills:
            for piece_start, piece_end in self._hill_pieces(
                distances, start, end, segment_length,
            ):
                run = distances[piece_end] - distances[piece_start]
                rise = altitudes[piece_end] - altitudes[piece_start]
                grade = rise / run * 100 if run > 0 else 0.0
                color = _grade_color(grade)
                piece = slice(piece_start, piece_end + 1)
                ax.fill_between(
                    km[piece], altitudes[piece], base,
                    color=color, edgecolor=color, lw=0.6, zorder=2,
                )
            ax.plot(
                km[start:end + 1], altitudes[start:end + 1],
                color=_TEXT, lw=1.6, zorder=4, solid_capstyle='round',
            )

        self._label_hills(ax, km, distances, altitudes, hills)

        # Recessive axes.
        ax.set_xlim(np.nanmin(km[valid]), np.nanmax(km[valid]))
        ax.set_ylim(base, highest + 0.32 * span)
        for side in ('top', 'right', 'left'):
            ax.spines[side].set_visible(False)
        ax.spines['bottom'].set_color(_TEXT_MUTED)
        ax.tick_params(colors=_TEXT_SECONDARY, labelsize=9, length=0, pad=6)
        ax.tick_params(axis='x', length=3, color=_TEXT_MUTED)
        ax.grid(False)
        ax.yaxis.grid(True, color=_GRID, lw=0.8)
        ax.set_axisbelow(True)
        ax.set_xlabel('Distance (km)', color=_TEXT_SECONDARY, fontsize=9.5)
        ax.set_ylabel('Altitude (m)', color=_TEXT_SECONDARY, fontsize=9.5)

        # Header: title, summary and grade legend.
        ax.set_title(
            title, loc='left', fontsize=13, fontweight='bold', color=_TEXT,
            pad=30,
        )
        ax.text(
            0, 1.035, self._hills_summary(altitudes, hills),
            transform=ax.transAxes, fontsize=9.5, color=_TEXT_SECONDARY,
            va='bottom',
        )
        handles = [
            Patch(color=color, label=label)
            for color, label in zip(HILL_GRADE_COLORS, HILL_GRADE_LABELS)
        ]
        handles.append(Patch(color=_TERRAIN, label='not a hill'))
        legend = ax.legend(
            handles=handles, title='Grade', ncol=len(handles),
            loc='lower right', bbox_to_anchor=(1, 1.02), frameon=False,
            fontsize=8.5, title_fontsize=8.5, handlelength=1.1,
            handleheight=0.9, columnspacing=1.1, handletextpad=0.5,
            alignment='left',
        )
        plt.setp(legend.get_texts(), color=_TEXT_SECONDARY)
        legend.get_title().set_color(_TEXT_SECONDARY)

        fig.tight_layout()
        return fig

    @staticmethod
    def _hill_pieces(
        distances: np.ndarray, start: int, end: int, segment_length: float,
    ) -> list:
        """Split the hill [start, end] into (first, last) index pairs of
        about segment_length meters each; a short tail is merged into the
        previous piece."""
        edges = [start]
        next_cut = distances[start] + segment_length
        for index in range(start + 1, end):
            if distances[index] >= next_cut:
                edges.append(index)
                next_cut = distances[index] + segment_length
        if (
            len(edges) > 1
            and distances[end] - distances[edges[-1]] < segment_length / 3
        ):
            edges.pop()
        edges.append(end)
        return list(zip(edges, edges[1:]))

    @staticmethod
    def _label_hills(
        ax, km: np.ndarray, distances: np.ndarray, altitudes: np.ndarray,
        hills: list,
    ) -> None:
        """Number every hill at its summit and, if there are not too many,
        add its elevation gain, length and average grade."""
        detailed = len(hills) <= _MAX_DETAILED_LABELS
        first, last = np.nanmin(km), np.nanmax(km)
        width = last - first
        for number, (start, end) in enumerate(hills, 1):
            position = (km[end] - first) / width if width else 0.5
            if position < 0.04:
                align, shift = 'left', -3
            elif position > 0.96:
                align, shift = 'right', 3
            else:
                align, shift = 'center', 0
            summit = (km[end], altitudes[end])
            ax.plot(
                *summit, 'o', ms=5, color=_TEXT, mec=_SURFACE, mew=1.5,
                zorder=5,
            )
            ax.annotate(
                str(number), summit, xytext=(shift, 9),
                textcoords='offset points', ha=align, va='bottom',
                fontsize=10, fontweight='bold', color=_TEXT, zorder=6,
            )
            if not detailed:
                continue
            gain = altitudes[end] - altitudes[start]
            length = distances[end] - distances[start]
            grade = gain / length * 100 if length > 0 else 0.0
            ax.annotate(
                f'+{gain:.0f} m\n{length / 1000:.1f} km · {grade:.1f} %',
                summit, xytext=(shift, 23), textcoords='offset points',
                ha=align, multialignment=align, va='bottom', fontsize=8.5,
                color=_TEXT_SECONDARY, linespacing=1.25, zorder=6,
            )

    @staticmethod
    def _hills_summary(altitudes: np.ndarray, hills: list) -> str:
        """One-line summary shown under the title."""
        valid = altitudes[~np.isnan(altitudes)]
        total_ascent = float(np.sum(np.clip(np.diff(valid), 0, None)))
        if not hills:
            return f'No hills identified  ·  {total_ascent:,.0f} m total ascent'
        climbed = sum(altitudes[end] - altitudes[start] for start, end in hills)
        noun = 'hill' if len(hills) == 1 else 'hills'
        return (
            f'{len(hills)} {noun}  ·  {climbed:,.0f} m climbed in hills'
            f'  ·  {total_ascent:,.0f} m total ascent'
        )

    def plot_intervals_in_map(
        self,
        timestamp: list,
        identified_intervals: list,
    ) -> plt:
        """Method for plotting all intervals identified
        in data on topographic map.\n
        Args:
            timestamp (list):
                list of timestamps
            identified_intervals (list):
                list of identified intervals
        Returns:
            plt (matplotlib.pyplot):
                plot of all intervals identified in data on topographic map.
        """
        x_points = []
        y_points = []

        points = self.get_positions_of_intervals(
            identified_intervals,
        )  # Getting positions of intervals

        # Appending points to lists
        for i in range(len(timestamp)):
            time = (
                    timestamp[i] - timestamp[0]
            ).total_seconds()
            # Calculation of time between the current and the starting point

            x_points.append(float(time))  # Appending the time to the list

            # If the current is in the list, it belongs to an interval
            if i > 0 and i in points:
                y_points.append(1)

                # If both current and previous point belong to
                # an interval, they are represented with red
                if y_points[i - 1] == y_points[i]:
                    plt.plot(
                        [x_points[i - 1], x_points[i]],
                        [y_points[i - 1], y_points[i]],
                        c='red',
                        linewidth=3,
                    )
            else:
                y_points.append(0)

                # If both current and previous point don't belong to
                # an interval, they are represented with blue
                if y_points[i - 1] == y_points[i]:
                    plt.plot(
                        [x_points[i - 1], x_points[i]],
                        [y_points[i - 1], y_points[i]],
                        c='blue',
                        linewidth=3,
                    )

        # Setting the parameters of the plot
        plt.xticks(fontsize=14)
        plt.yticks([0, 1], ['No', 'Yes'])
        plt.title('Intervals', fontsize=20)
        plt.xlabel('Time (s)', fontsize=20)
        plt.ylabel('Interval', fontsize=20)
        return plt

    def plot_basic_map(self, altitude: list, distance: list) -> plt:
        """Method for plotting the whole topographic map.\n
        Args:
            altitude (list):
                list of altitudes
            distance (list):
                list of distances
        Returns:
            plt (matplotlib.pyplot):
                plot of the whole topographic map.
        """
        ax = plt.axes()
        y = []
        x = []

        for j in range(len(distance)):
            y.append(float(altitude[j]))
            x.append(float(distance[j]))

            ax.plot(x[j], y[j], 'o', color='b', markersize=2)

        plt.xticks(fontsize=14)
        plt.title('Topographic map of cycling activity', fontsize=20)
        plt.xlabel('Distance (m)', fontsize=20)
        plt.ylabel('Altitude (m)', fontsize=20)
        return plt

    def get_color_for_incline(self, x1, x2, y1, y2) -> str:
        dy = y2 - y1
        dx = x2 - x1

        if dx == 0.0:
            incline = 0.0
        else:
            incline = (dy / dx) * 100

        incline = abs(incline)

        if incline == 0.0:
            return '#5FD67B'
        elif 0 < incline <= 2.9:
            return '#43C160'
        elif 2.9 < incline <= 5.9:
            return '#28A745'
        elif 5.9 < incline <= 8.9:
            return '#159231'
        elif incline > 8.9:
            return '#087621'
        else:
            return '#000000'
