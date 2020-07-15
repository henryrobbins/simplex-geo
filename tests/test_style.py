import pytest
import numpy as np
import gilp.style as st
import plotly.graph_objects as plt


# The following functions are not tested since they create visual objects:
# table, vector, scatter, line, equation, and polygon


@pytest.mark.parametrize("n,s",[
    (1.0, '1'),
    (1.0001, '1'),
    (1.023, '1.023'),
    (0.0, '0'),
    (3.45667777, '3.457'),
    (2.00000005, '2'),
    (1.9999999, '2')])
def test_format(n,s):
    assert st.format(n) == s


@pytest.mark.parametrize("A,i,c,s",[
    (np.array([1,2,3]), [2,4,6], None,
     '1x<sub>2</sub> + 2x<sub>4</sub> + 3x<sub>6</sub>'),
    (np.array([1.000001,-1.9999999,0.00]), [1,2,3], None,
     '1x<sub>1</sub> - 2x<sub>2</sub> + 0x<sub>3</sub>'),
    (np.array([-1,-3,11]), [1,3,6], None,
     '-1x<sub>1</sub> - 3x<sub>3</sub> + 11x<sub>6</sub>'),
    (np.array([-3,4]), [1,3], 1,
     '1 - 3x<sub>1</sub> + 4x<sub>3</sub>')])
def test_linear_string(A,i,c,s):
    assert st.linear_string(A,i,c) == s


@pytest.mark.parametrize("A,b,comp,s",[
    (np.array([1,2,3]), 4, " = ",
     '1x<sub>1</sub> + 2x<sub>2</sub> + 3x<sub>3</sub> = 4'),
    (np.array([2.8999999,1.66666,-3.33333]), 17, " ≤ ",
     '2.9x<sub>1</sub> + 1.667x<sub>2</sub> - 3.333x<sub>3</sub> ≤ 17')])
def test_equation_string(A,b,comp,s):
    assert st.equation_string(A,b,comp) == s


@pytest.mark.parametrize("d,s",[
    (dict(BFS=[2.990,4.567,0.00001,1.0001],
          B=[3,6,4],
          Obj=1567.3456),
     "<b>BFS</b>: (2.99, 4.567, 0, 1)<br>"
     + "<b>B</b>: (3, 6, 4)<br>"
     + "<b>Obj</b>: 1567.346"),
    (dict(BFS=[1.0001,3.99999,0.00001,1.0001],
          B=[4,5,6],
          Obj=-17.8900),
     "<b>BFS</b>: (1, 4, 0, 1)<br>"
     + "<b>B</b>: (4, 5, 6)<br>"
     + "<b>Obj</b>: -17.89")])
def test_label(d,s):
    assert st.label(d) == s


def test_axis_bad_inputs():
    fig = plt.Figure()
    with pytest.raises(ValueError, match='.*vectors of length 2 or 3'):
        st.set_axis_limits(fig,[np.array([[2],[3],[4],[5]])])
    with pytest.raises(ValueError, match='.*only retrieve 2 or 3 axis limits'):
        st.get_axis_limits(fig,4)


@pytest.mark.parametrize("x_list,n,limits",[
    ([np.array([[0],[1]]),
      np.array([[1],[1]]),
      np.array([[0.5],[1]]),
      np.array([[0.5],[0.5]]),
      np.array([[1],[2]])],
     2,[1.3,2.6]),
    ([np.array([[0],[1],[1]]),
      np.array([[1],[0],[2]]),
      np.array([[0],[3],[1]]),
      np.array([[1],[1],[0]]),
      np.array([[0],[2],[1]])],
     3,[1.3,3.9,2.6])])
def test_axis_limits(x_list,n,limits):
    fig = plt.Figure()
    st.set_axis_limits(fig,x_list)
    assert np.allclose(st.get_axis_limits(fig,n),limits,atol=1e-7)


def test_intersection_bad_inputs():
    with pytest.raises(ValueError, match='.* supports equations in 2 or 3 .*'):
        A = np.array([4,1,5,6])
        b = 6
        D = np.array([[1,1],[0,1],[1,-1],[1,0],[-2,1]])
        e = np.array([[6],[4],[2],[3],[0]])
        st.intersection(A,b,D,e)


# TODO: Find way to compare where order does not matter
@pytest.mark.parametrize("A,b,pts",[
    (np.array([4,1]), 6,
     [np.array([[1],[2]]), np.array([[1.5],[0]])]),
    (np.array([4,5]), 7,
     [np.array([[0.5],[1]]),np.array([[1.75],[0]])])])
def test_intersection_2d(A,b,pts):
    D = np.array([[1,1],[0,1],[1,-1],[1,0],[-2,1]])
    e = np.array([[6],[4],[2],[3],[0]])
    actual = st.intersection(A,b,D,e)
    assert all(np.allclose(x,y,atol=1e-7) for x,y in zip(actual, pts))


@pytest.mark.parametrize("A,b,pts",[
    (np.array([0,0,1]), 0.5,
     [np.array([[1],[1],[0.5]]),
      np.array([[1],[0],[0.5]]),
      np.array([[0],[1],[0.5]]),
      np.array([[0],[0],[0.5]])]),
    (np.array([2,0,1]), 1.5,
     [np.array([[0.25],[1],[1]]),
      np.array([[0.75],[1],[0]]),
      np.array([[0.25],[0],[1]]),
      np.array([[0.75],[0],[0]])])])
def test_intersection_3d(A,b,pts):
    D = np.array([[1,0,0],[0,1,0],[0,0,1]])
    e = np.array([[1],[1],[1]])
    actual = st.intersection(A,b,D,e)
    assert all(np.allclose(x,y,atol=1e-7) for x,y in zip(actual, pts))


def test_order_bad_inputs():
    with pytest.raises(ValueError, match='.*must be represented by column.*'):
        st.order([np.array([[1,2,3]])])
    with pytest.raises(ValueError, match='.*must be 2 or 3 dimensional'):
        st.order([np.array([[1],[2],[3],[4]])])


@pytest.mark.parametrize("x_list,pts",[
    ([np.array([[3],[3]]),
      np.array([[2],[4]]),
      np.array([[2],[0]]),
      np.array([[0],[0]]),
      np.array([[3],[1]])],
     [[2,0,2,3,3],[4,0,0,1,3]]),
    ([np.array([[3],[3]]),
      np.array([[2],[4]])],
     [[2,3],[4,3]]),
    ([np.array([[1],[4]])],
     [[1],[4]])])
def test_order_2d(x_list,pts):
    assert st.order(x_list) == pts


@pytest.mark.parametrize("x_list,pts",[
    ([np.array([[-1.7],[0],[0.59]]),
      np.array([[0],[-0.59],[1.7]]),
      np.array([[0],[0.59],[1.7]]),
      np.array([[-1],[-1],[1]]),
      np.array([[-1],[1],[1]])],
     [[0,0,-1,-1.7,-1,0],
      [-0.59,0.59,1,0,-1,-0.59],
      [1.7,1.7,1,0.59,1,1.7]]),
    ([np.array([[0],[1],[0]]),
      np.array([[-0.5],[0],[0.5]]),
      np.array([[0.5],[0],[0.5]])],
     [[-0.5,0,0.5,-0.5],
      [0,1,0,0],
      [0.5,0,0.5,0.5]])])
def test_order_3d(x_list,pts):
    assert st.order(x_list) == pts