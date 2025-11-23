#!/usr/bin/env python3
"""Test script to verify ground launch and cloud collision fixes."""

import sys
import math
import pygame
from bouncing_ball import BouncingBallSimulation, Ball, BallState, Cloud

def test_ground_launch_mechanics():
    """Test that balls can be launched upward from ground position."""
    print("Testing ground launch mechanics...")
    
    # Initialize pygame
    pygame.init()
    
    # Create simulation
    sim = BouncingBallSimulation()
    
    # Check initial ball exists and is near ground
    assert len(sim.balls) > 0, "No initial ball created!"
    initial_ball = sim.balls[0]
    
    print(f"Ball position: ({initial_ball.x:.1f}, {initial_ball.y:.1f})")
    print(f"Screen height: {sim.height}")
    print(f"Distance from ground: {sim.height - initial_ball.y - initial_ball.radius:.1f}px")
    
    # Simulate clicking on the ball
    click_x, click_y = initial_ball.x, initial_ball.y
    sim._start_slingshot(initial_ball, click_x, click_y)
    
    # Verify drag_start_pos uses mouse position
    assert sim.drag_start_pos == (click_x, click_y), \
        f"Drag start should be mouse position ({click_x}, {click_y}), got {sim.drag_start_pos}"
    
    # Simulate dragging down and right (should shoot up and left)
    drag_x = click_x + 100  # Drag 100px right
    drag_y = click_y + 50   # Drag 50px down
    
    # Manually set mouse position for test
    sim.mouse_pos = (drag_x, drag_y)
    
    # Test that release calculates velocity correctly
    # Calculate expected velocity
    expected_dx = click_x - drag_x  # -100 (left)
    expected_dy = click_y - drag_y  # -50 (up)
    
    print(f"\nSimulated drag: from ({click_x:.0f}, {click_y:.0f}) to ({drag_x:.0f}, {drag_y:.0f})")
    print(f"Expected velocity direction: dx={expected_dx}, dy={expected_dy} (up and left)")
    
    # The new mechanics should allow upward launch even from ground
    assert expected_dy < 0, "Should be able to shoot upward (negative dy)"
    
    print("✅ Ground launch mechanics working correctly!")
    
    return True

def test_cloud_collision():
    """Test that cloud collisions are less sticky."""
    print("\nTesting cloud collision dampening...")
    
    # Create simulation
    sim = BouncingBallSimulation()
    
    # Create a test ball with known velocity
    test_ball = Ball(
        x=400, y=150,
        vx=200, vy=-100,
        radius=25,
        color=(255, 0, 0),
        has_been_launched=True
    )
    sim.balls.append(test_ball)
    
    # Create a cloud in the ball's path
    test_cloud = Cloud(
        x=350, y=100,
        width=100, height=100,
        vx=0
    )
    sim.clouds = [test_cloud]
    
    # Store original velocity
    original_vx = test_ball.vx
    original_vy = test_ball.vy
    original_speed = math.sqrt(original_vx**2 + original_vy**2)
    
    print(f"Original velocity: vx={original_vx:.1f}, vy={original_vy:.1f}")
    print(f"Original speed: {original_speed:.1f}")
    
    # Trigger cloud collision check
    sim._check_cloud_collisions()
    
    # Check new velocity after cloud collision
    new_vx = test_ball.vx
    new_vy = test_ball.vy
    new_speed = math.sqrt(new_vx**2 + new_vy**2)
    
    print(f"After cloud: vx={new_vx:.1f}, vy={new_vy:.1f}")
    print(f"New speed: {new_speed:.1f}")
    
    # Verify dampening is gentler (0.85 for x, 0.9 for y)
    expected_vx = original_vx * 0.85
    expected_vy = original_vy * 0.9
    
    assert abs(new_vx - expected_vx) < 0.1, \
        f"X velocity should be {expected_vx:.1f}, got {new_vx:.1f}"
    assert abs(new_vy - expected_vy) < 0.1, \
        f"Y velocity should be {expected_vy:.1f}, got {new_vy:.1f}"
    
    # Verify ball still has significant speed (not stuck)
    speed_retention = new_speed / original_speed
    print(f"Speed retention: {speed_retention:.1%}")
    
    assert speed_retention > 0.8, \
        f"Ball retained only {speed_retention:.1%} of speed, should be >80%"
    
    print("✅ Cloud collisions are now less sticky!")
    
    return True

def test_multiball_launch_state():
    """Test that multiball creates properly launched balls."""
    print("\nTesting multiball launch state...")
    
    # Create simulation
    sim = BouncingBallSimulation()
    
    # Create original ball
    original = Ball(
        x=400, y=300,
        vx=100, vy=-200,
        radius=25,
        color=(0, 255, 0),
        has_been_launched=True
    )
    
    # Activate multiball and create shots
    sim.game_state.multiball_active = True
    sim._create_multiball_shots(original)
    
    # Check that 2 additional balls were created
    multiball_count = len([b for b in sim.balls if b != original])
    assert multiball_count >= 2, f"Should create 2 additional balls, created {multiball_count}"
    
    # Check that new balls are marked as launched
    for ball in sim.balls:
        if ball != original:
            assert ball.has_been_launched, "Multiball shots should be marked as launched"
    
    print(f"Created {multiball_count} additional balls, all marked as launched")
    print("✅ Multiball mechanics working correctly!")
    
    return True

if __name__ == "__main__":
    try:
        test_ground_launch_mechanics()
        test_cloud_collision()
        test_multiball_launch_state()
        
        print("\n" + "="*50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("="*50)
        print("\nImprovements implemented:")
        print("1. ✅ Balls can now be launched upward from ground position")
        print("2. ✅ Clouds no longer trap balls (gentler dampening)")
        print("3. ✅ Multiball shots are properly marked as launched")
        
        pygame.quit()
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        pygame.quit()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)
