import pytest
from chatbot.memory import SlidingWindowMemory

def test_sliding_window_memory_initialization():
    mem = SlidingWindowMemory(max_turns=2)
    assert len(mem.get_history()) == 0

def test_sliding_window_adds_messages():
    mem = SlidingWindowMemory(max_turns=2)
    mem.add_user_message("Hello")
    history = mem.get_history()
    
    assert len(history) == 1
    assert history[0]["role"] == "user"
    assert history[0]["parts"][0] == "Hello"

def test_sliding_window_drops_oldest():
    # max_turns=1 means only 1 user+model pair is kept
    mem = SlidingWindowMemory(max_turns=1)
    
    mem.add_user_message("Q1")
    mem.add_model_message("A1")
    
    assert len(mem.get_history()) == 2
    
    mem.add_user_message("Q2")
    mem.add_model_message("A2")
    
    history = mem.get_history()
    
    # Should only keep Q2 and A2
    assert len(history) == 2
    assert history[0]["parts"][0] == "Q2"
    assert history[1]["parts"][0] == "A2"

def test_clear_memory():
    mem = SlidingWindowMemory(max_turns=2)
    mem.add_user_message("Hello")
    mem.clear()
    assert len(mem.get_history()) == 0
