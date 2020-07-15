import pytest
import gilp.visualize as vs


# The following functions are not tested since they create visual objects:
# set_up_fig, plot_lp, add_path, add_isoprofits, add_tableaus, simplex_visual


def test_set_up_figure():
    with pytest.raises(ValueError, match='.*visualize 2 or 3 dimensional.*'):
        vs.set_up_figure(4)


def test_plot_lp(unbounded_lp):
    with pytest.raises(vs.InfiniteFeasibleRegion):
        vs.plot_lp(unbounded_lp)


def test_get_tableau_strings(degenerate_lp):
    B = [0,1,4,5,6]
    canonical_head = ['<b>z<sub></sub></b>', '<b>x<sub>1</sub></b>',
                      '<b>x<sub>2</sub></b>', '<b>x<sub>3</sub></b>',
                      '<b>x<sub>4</sub></b>', '<b>x<sub>5</sub></b>',
                      '<b>x<sub>6</sub></b>', '<b>x<sub>7</sub></b>',
                      '<b>RHS<sub></sub></b>']
    canonical_cont = [['1<br>0<br>0<br>0<br>0<br>0'],
                      ['0<br>1<br>0<br>0<br>0<br>0'],
                      ['0<br>0<br>1<br>0<br>0<br>0'],
                      ['-1<br>1<br>0<br>-1<br>-1<br>2'],
                      ['-1<br>-1<br>1<br>2<br>1<br>-3'],
                      ['0<br>0<br>0<br>1<br>0<br>0'],
                      ['0<br>0<br>0<br>0<br>1<br>0'],
                      ['0<br>0<br>0<br>0<br>0<br>1'],
                      ['10<br>2<br>4<br>4<br>1<br>0']]
    dictionary_head = ['<b>ITERATION 3</b>',' ', ' ']
    dictionary_cont = [['max<br>subject to<br> <br> <br> <br> '],
                       [' <br>x<sub>1</sub><br>x<sub>2</sub><br>x<sub>5</sub>'
                        + '<br>x<sub>6</sub><br>x<sub>7</sub>'],
                       ['10 - 1x<sub>3</sub> - 1x<sub>4</sub><br>'
                        + '= 2 - 1x<sub>3</sub> + 1x<sub>4</sub><br>'
                        + '= 4 + 0x<sub>3</sub> - 1x<sub>4</sub><br>'
                        + '= 4 + 1x<sub>3</sub> - 2x<sub>4</sub><br>'
                        + '= 1 + 1x<sub>3</sub> - 1x<sub>4</sub><br>'
                        + '= 0 - 2x<sub>3</sub> + 3x<sub>4</sub>']]

    actual = vs.get_tableau_strings(degenerate_lp,B,3,'canonical')
    assert canonical_head == actual[0]
    assert canonical_cont == actual[1]
    actual = vs.get_tableau_strings(degenerate_lp,B,3,'dictionary')
    assert dictionary_head == actual[0]
    assert dictionary_cont == actual[1]