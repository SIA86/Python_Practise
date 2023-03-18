from tictactoe import *
import pytest


def test_player():

    assert player([[EMPTY,EMPTY,EMPTY],[EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == X
    assert player([[X,O,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == X
    assert player([[X,O,X], [O,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == X
    assert player([[X,O,X], [O,X,O], [EMPTY,EMPTY,EMPTY]]) == X
    assert player([[X,O,X], [O,X,O], [X,O,EMPTY]]) == X

    assert player([[X,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == O
    assert player([[X,O,X], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == O
    assert player([[X,O,X], [O,X,EMPTY], [EMPTY,EMPTY,EMPTY]]) == O
    assert player([[X,O,X], [O,X,O], [X,EMPTY,EMPTY]]) == O

def test_actions():

    assert actions([[EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == {(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)}
    assert actions([[X,O,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == {(0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)}
    assert actions([[X,O,X], [O,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == {(1,1), (1,2), (2,0), (2,1), (2,2)}
    assert actions([[X,O,X], [O,X,O], [EMPTY,EMPTY,EMPTY]]) == {(2,0), (2,1), (2,2)}
    assert actions([[X,O,X], [O,X,O], [X,O,EMPTY]]) == {(2,2)}

    assert actions([[X,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == {(0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)}
    assert actions([[X,O,X], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == {(1,0), (1,1), (1,2), (2,0), (2,1), (2,2)}
    assert actions([[X,O,X], [O,X,EMPTY], [EMPTY,EMPTY,EMPTY]]) == {(1,2), (2,0), (2,1), (2,2)}
    assert actions([[X,O,X], [O,X,O], [X,EMPTY,EMPTY]]) == {(2,1), (2,2)}


def test_result():
    assert result([[EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]], (0, 0)) == [[X,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]
    assert result([[X,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]], (0, 1)) == [[X,O,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]
    assert result([[X,O,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]], (0, 2)) == [[X,O,X], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]
    assert result([[X,O,EMPTY], [X,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]], (1,1)) == [[X,O,EMPTY], [X,O,EMPTY], [EMPTY,EMPTY,EMPTY]]


def test_Exception():
    with pytest.raises(Exception):
        assert result([[X,O,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]], (0, 1))
        assert result([[X,O,X], [X,O,EMPTY], [EMPTY,EMPTY,EMPTY]], (1, 1))

def test_winner():
    assert winner([[X,O,X], [X,O,O], [X,EMPTY,EMPTY]]) == X
    assert winner([[X,X,X], [EMPTY,O,O], [EMPTY,EMPTY,EMPTY]]) == X

    assert winner([[X,O,X], [EMPTY,O,O], [X,O,X]]) == O
    assert winner([[X,X,EMPTY], [O,O,O], [X,EMPTY,EMPTY]]) == O

    assert winner([[X,O,X], [X,O,X], [O,X,O]]) == None
    assert winner([[O,X,X], [X,O,O], [O,X,X]]) == None


def test_terminal():
    assert terminal([[EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == 0
    assert terminal([[X,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == 0
    assert terminal([[X,O,EMPTY], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == 0
    assert terminal([[X,O,X], [EMPTY,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == 0
    assert terminal([[X,O,X], [O,EMPTY,EMPTY], [EMPTY,EMPTY,EMPTY]]) == 0

    assert terminal([[X,X,X], [O,EMPTY,EMPTY], [EMPTY,O,EMPTY]]) == 1
    assert terminal([[X,O,X], [X,EMPTY,O], [X,O,EMPTY]]) == 1
    assert terminal([[O,O,X], [X,O,O], [X,O,X]]) == 1
    assert terminal([[X,X,X], [X,O,O], [O,O,X]]) == 1


    assert terminal([[X,O,X], [X,O,X], [O,X,O]]) == 1
    assert terminal([[O,X,X], [X,O,O], [O,X,X]]) == 1
    assert terminal([[X,X,O], [O,O,X], [X,X,O]]) == 1


def test_utility():
    assert utility([[X,X,O], [O,O,X], [X,X,O]]) == 0
    assert utility([[X,O,X], [X,O,X], [O,X,O]]) == 0
    assert utility([[O,X,X], [X,O,O], [O,X,X]]) == 0

    assert utility([[X,X,X], [O,EMPTY,EMPTY], [EMPTY,O,EMPTY]]) == 1
    assert utility([[X,O,X], [X,EMPTY,O], [X,O,EMPTY]]) == 1
    assert utility([[X,X,X], [X,O,O], [O,O,X]]) == 1

    assert utility([[O,O,X], [X,O,O], [X,O,X]]) == -1
    assert utility([[O,O,O], [X,X,O], [X,X,EMPTY]]) == -1
    assert utility([[EMPTY,X,O], [EMPTY,X,O], [X,EMPTY,O]]) == -1


def test_minimax():
    assert minimax([[X,X,O], [O,O,X], [X,X,O]]) == None
    assert minimax([[X,O,X], [X,O,X], [O,X,O]]) == None
    assert minimax([[O,X,X], [X,O,O], [O,X,X]]) == None

    assert minimax([[X,X,O],
                    [O,X,EMPTY],
                    [O,EMPTY,EMPTY]]) == (1,2)
    assert minimax([[X,X,EMPTY],
                    [O,X,EMPTY],
                    [O,O,EMPTY]]) == (0,2) or (2,2)

