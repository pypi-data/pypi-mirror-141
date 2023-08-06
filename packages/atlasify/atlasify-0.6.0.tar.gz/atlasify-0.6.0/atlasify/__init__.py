"""
The atlasify package provides the method atlasify() which applies ATLAS style
to matplotlib plots.
"""

# Copyright (C) 2019-2022 Frank Sauerburger
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import os.path
from packaging import version

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.transforms import ScaledTranslation, IdentityTransform
from matplotlib import font_manager

__version__ = '0.6.0'

def _setup_mpl():
    """
    Set sensible default values for matplotlib mainly concerning fonts.
    """
    # Add internal font directory
    font_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fonts")
    font_files = font_manager.findSystemFonts(fontpaths=[font_dir])

    new_fonts = []
    try:
        # For mpl 3.2 and higher
        for font_file in font_files:
            # Resemble add_font
            font = mpl.ft2font.FT2Font(font_file)
            prop = font_manager.ttfFontProperty(font)
            new_fonts.append(prop)
    except AttributeError:
        # Legacy
        # pylint: disable=no-member
        new_fonts = font_manager.createFontList(font_files)

    # Give precedence to fonts shipped in this package
    font_manager.fontManager.ttflist = new_fonts \
                                       + font_manager.fontManager.ttflist

    # Change font
    mpl.rcParams['font.family'] = 'sans-serif'
    mpl.rcParams['font.sans-serif'] = ['Helvetica', 'Nimbus Sans',
                                       'Nimbus Sans L', 'Arial']

    # Disable Unicode minus signs for incompatible mpl versions
    if version.parse(mpl.__version__) < version.parse("3.3"):
        mpl.rcParams['axes.unicode_minus'] = False

_setup_mpl()

ATLAS = "ATLAS"
LINE_SPACING = 1.2
MAJOR_TICK_LENGTH = 6
MINOR_TICK_LENGTH = 3
OFFSET = 5
INDENT = 8


PT = 1 / 72  # 1 point in inches

def enlarge_yaxis(axes, factor=1):
    """
    Enlarges the y-axis by the given factor. A factor of 1 has no effect. The
    lower boundary of the y-axis is not affected.
    """
    ylim = axes.get_ylim()
    y_upper = ylim[0] + (ylim[1] - ylim[0]) * factor
    axes.set_ylim((ylim[0], y_upper))


def _indent(outside):
    """
    Return the base point indent of the ATLAS badge.
    """
    return (2 + (0 if outside else INDENT)) * PT

def _offset(outside, subtext, font_size, sub_font_size):
    """
    Return the vertical offset of the base point of the ATLAS badge.
    """
    offset = -(OFFSET + font_size)  # Inside

    if outside:
        offset = OFFSET  # Outside
        if isinstance(subtext, str):
            offset += LINE_SPACING * sub_font_size * (subtext.count("\n") + 1)

    return offset * PT

def atlasify_legend(axes):
    """
    Removes the frame from existing legend and enables legend if there are
    more then two handles. The location of a pre-exisitng legend is not
    changed.
    """
    handles, _ = axes.get_legend_handles_labels()
    legend = axes.get_legend()

    if legend is not None:
        # Remove frame from pre-existing legend
        legend.set_frame_on(False)
    elif len(handles) >= 2:
        # Automatically enable legend if there are more the two handles
        axes.legend(frameon=False, loc=1)

_ORIG_SET_XLABEL = mpl.axes.Axes.set_xlabel
def set_xlabel(axes, label, *args, **kwargs):
    """
    Set an x-label on a plot, and align it to the right. All arguments are
    forwarded.
    """
    kwargs_ = dict(x=1.0, ha="right")
    kwargs_.update(kwargs)
    _ORIG_SET_XLABEL(axes, label, *args, **kwargs_)

_ORIG_SET_YLABEL = mpl.axes.Axes.set_ylabel
def set_ylabel(axes, label, *args, **kwargs):
    """
    Set an y-label on a plot, and align it to the top. All arguments are
    forwarded.
    """
    kwargs_ = dict(y=1.0, ha="right")
    kwargs_.update(kwargs)
    _ORIG_SET_YLABEL(axes, label, *args, **kwargs_)

def monkeypatch_axis_labels():
    """
    Monkeypatch the `matplotlib.axes.Axes.set_(xy)labels` methods to have
    default alignment top and right.
    """
    mpl.axes.Axes.set_xlabel = set_xlabel
    mpl.axes.Axes.set_ylabel = set_ylabel

# pylint: disable=R0913,R0914
def atlasify(atlas=True, subtext: str = None, enlarge: float = None,
             axes: mpl.axes = None, outside: bool = False, font_size: int = 16,
             label_font_size: int = 16, sub_font_size: int = 12):
    """
    Applies the atlas style to the plot.

    Parameters
    ----------
    atlas : str or bool, optional
        If the argument evaluates to true, the ATLAS badge is added. If a non-empty
        string is provided, the string is appended after the badge, by default True
    subtext : str, optional
        Text which is put below the badge. Multiple lines are printed separately.
        By default None
    enlarge : float, optional
        Defines how far the y-axis should be extended to accommodate for the badge.
        By default, this is set to 1.3 if outside is False.
    axes : matplotlib.axes, optional
        Axis you want to atlasify. By default, the currently active axis is used
    outside : bool, optional
        If True, the label will be placed above the plot. By default False
    font_size : int, optional
        Font size of the ATLAS badge itself, by default 16
    label_font_size : int, optional
        Font size of the text after the badge, by default 16
    sub_font_size : int, optional
        Font size of the subtext, by default 12
    """
    if enlarge is None:
        enlarge = 1 + 0.3 * (not outside)

    if axes is None:
        axes = plt.gca()

    enlarge_yaxis(axes, enlarge)
    atlasify_legend(axes)

    axes.tick_params("both", which="both", direction="in")
    axes.tick_params("both", which="major", length=MAJOR_TICK_LENGTH)
    axes.tick_params("both", which="minor", length=MINOR_TICK_LENGTH)
    axes.tick_params("x", which="both", top=True)
    axes.tick_params("y", which="both", right=True)
    axes.xaxis.set_minor_locator(AutoMinorLocator())
    axes.yaxis.set_minor_locator(AutoMinorLocator())


    trans_indent = ScaledTranslation(_indent(outside), 0,
                                     axes.figure.dpi_scale_trans)
    trans_top = ScaledTranslation(0,
                                  _offset(outside, subtext, font_size, sub_font_size),
                                  axes.figure.dpi_scale_trans)

    trans_sub = IdentityTransform()

    has_branding = bool(atlas)
    if has_branding:
        badge = axes.text(0, 1, ATLAS,
                          transform=axes.transAxes + trans_indent + trans_top,
                          fontdict={"size": font_size,
                                    "style": "italic",
                                    "weight": "bold", })

        if isinstance(atlas, str):
            # Convert label width to dpi independent unit (pre-render)
            renderer = mpl.backends.backend_agg.FigureCanvasAgg(axes.figure).get_renderer()

            # in display units, i.e., pixel
            box = badge.get_window_extent(renderer)
            box = axes.figure.dpi_scale_trans.inverted() \
                      .transform(box)  # in inch
            badge_width = box[1][0] - box[0][0]

            trans_info = ScaledTranslation(0.23 * font_size * PT + badge_width,
                                           0, axes.figure.dpi_scale_trans)
            axes.text(0, 1, atlas,
                      transform=axes.transAxes + trans_indent + trans_top +
                      trans_info, fontdict={"size": label_font_size, })

    if isinstance(subtext, str):
        trans_sub += ScaledTranslation(
            0, -LINE_SPACING * sub_font_size * PT * has_branding,
            axes.figure.dpi_scale_trans
        )

        for line in subtext.split("\n"):
            axes.text(0, 1, line,
                      transform=axes.transAxes + trans_indent + trans_top +
                      trans_sub, fontdict={"size": sub_font_size, })
            trans_sub += ScaledTranslation(0, -LINE_SPACING * sub_font_size * PT,
                                           axes.figure.dpi_scale_trans)
