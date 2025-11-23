#!/usr/bin/env python3
"""Test script to verify the ball positioning fix for the bird hunter game."""

import sys
import pygame
from bouncing_ball import BouncingBallSimulation, DisplayConstants

def test_ball_position():
    """Test that the initial ball is positioned correctly for slingshot aiming."""
    print("Testing ball position fix...")
    
    # Initialize pygame
    pygame.init()
    
    # Create simulation
    sim = BouncingBallSimulation()
    
    # Check initial ball exists
    assert len(sim.balls) > 0, "No initial ball created!"
    initial_ball = sim.balls[0]
    
    # Check ball position (should be at 40% from bottom)
    expected_y = sim.height - (sim.height * 0.4)
    actual_y = initial_ball.y
    
    print(f"Screen height: {sim.height}")
    print(f"Expected Y position (40% from bottom): {expected_y}")
    print(f"Actual Y position: {actual_y}")
    print(f"Distance from bottom: {sim.height - actual_y}")
    print(f"Percentage from bottom: {((sim.height - actual_y) / sim.height) * 100:.1f}%")
    
    # Verify the ball is positioned correctly (with some tolerance)
    tolerance = 10
    assert abs(actual_y - expected_y) < tolerance, \
        f"Ball position incorrect! Expected ~{expected_y}, got {actual_y}"
    
    # Verify there's enough room to drag down (at least 30% of screen height)
    room_below = sim.height - actual_y - initial_ball.radius
    min_room_needed = sim.height * 0.3
    assert room_below >= min_room_needed, \
        f"Not enough room below ball for dragging! Only {room_below}px available, need {min_room_needed}px"
    
    # Test reset functionality
    print("\nTesting reset functionality...")
    sim.reset_game()
    
    # Check ball exists after reset
    assert len(sim.balls) > 0, "No ball created after reset!"
    reset_ball = sim.balls[0]
    
    # Check reset ball position
    reset_y = reset_ball.y
    print(f"Ball Y position after reset: {reset_y}")
    assert abs(reset_y - expected_y) < tolerance, \
        f"Ball position incorrect after reset! Expected ~{expected_y}, got {reset_y}"
    
    print("\n✅ All tests passed!")
    print("The ball is now positioned correctly to allow upward shooting.")
    
    pygame.quit()
    return True

if __name__ == "__main__":
    try:
        test_ball_position()
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
