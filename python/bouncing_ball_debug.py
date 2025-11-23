#!/usr/bin/env python3
"""
DEBUGGING VERSION OF BOUNCING BALL WITH EXTENSIVE LOGGING
This version logs EVERYTHING for debugging purposes
"""

import pygame
import math
import random
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

# Import the main game components
from bouncing_ball import BouncingBallSimulation, Ball, BallState, Colors

# Override the main simulation class with extensive logging
class DebugBouncingBallSimulation(BouncingBallSimulation):
    def __init__(self, width=800, height=600):
        print("\n" + "="*80)
        print("🔴 DEBUG MODE ACTIVATED - EXTENSIVE LOGGING ENABLED 🔴")
        print("="*80)
        print(f"📊 Every user action will be logged")
        print(f"📍 Every ball position will be tracked")
        print(f"🎯 Every collision will be reported")
        print(f"🖱️ Every mouse event will be captured")
        print("="*80 + "\n")
        
        super().__init__(width, height)
        
        # Log initial state
        print("\n🏀 INITIAL GAME STATE")
        print(f"   Balls: {len(self.balls)}")
        print(f"   Ammo: {self.game_state.ammo_count}")
        
        if len(self.balls) > 0:
            for i, ball in enumerate(self.balls):
                print(f"   Ball {i}: pos=({ball.x:.0f},{ball.y:.0f}), state={ball.state}")
                print(f"            max_vx={ball.max_vx:.0f}, max_vy={ball.max_vy:.0f}")
        
        # Log frame counter
        self.frame_count = 0
        self.last_log_time = time.time()
        
    def handle_events(self) -> bool:
        """Handle events with extensive logging."""
        for event in pygame.event.get():
            # Log EVERY event
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"\n🖱️ MOUSE DOWN: Button {event.button} at {event.pos}")
                self._log_game_state("BEFORE MOUSE DOWN")
            elif event.type == pygame.MOUSEBUTTONUP:
                print(f"\n🖱️ MOUSE UP: Button {event.button} at {event.pos}")
                self._log_game_state("BEFORE MOUSE UP")
            elif event.type == pygame.MOUSEMOTION:
                # Log mouse motion only when dragging
                if self.dragging_ball:
                    print(f"🖱️ MOUSE DRAG: Position {event.pos}")
            elif event.type == pygame.KEYDOWN:
                print(f"\n⌨️ KEY DOWN: {pygame.key.name(event.key)}")
            
            # Call parent handler
            if not super().handle_events():
                return False
                
            # Log state after handling
            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]:
                self._log_game_state("AFTER EVENT HANDLING")
                
        return True
    
    def _handle_mouse_down(self, event):
        """Override to add logging."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print(f"\n🎯 ATTEMPTING TO GRAB BALL AT ({mouse_x}, {mouse_y})")
        
        # Check each ball
        for i, ball in enumerate(self.balls):
            distance = math.sqrt((mouse_x - ball.x)**2 + (mouse_y - ball.y)**2)
            print(f"   Ball {i}: pos=({ball.x:.0f},{ball.y:.0f}), distance={distance:.1f}, radius={ball.radius}")
            print(f"   Hit test: {distance} <= {ball.radius + 10}? {distance <= ball.radius + 10}")
            
            if distance <= ball.radius + 10:
                print(f"   ✅ GRABBED BALL {i}!")
                self.dragging_ball = ball
                self.drag_start_pos = (mouse_x, mouse_y)
                self.mouse_pos = (mouse_x, mouse_y)
                ball.state = BallState.GRABBED
                ball.vx = 0
                ball.vy = 0
                print(f"   Ball state: {ball.state}")
                print(f"   Drag start: {self.drag_start_pos}")
                return
        
        print(f"   ❌ NO BALL FOUND NEAR CLICK")
    
    def _handle_mouse_up(self, event):
        """Override to add logging."""
        if self.dragging_ball:
            print(f"\n🚀 RELEASING SLINGSHOT")
            print(f"   Ball position: ({self.dragging_ball.x:.0f}, {self.dragging_ball.y:.0f})")
            print(f"   Mouse position: {self.mouse_pos}")
            print(f"   Drag start: {self.drag_start_pos}")
            
            # Calculate launch
            dx = self.drag_start_pos[0] - self.mouse_pos[0]
            dy = self.drag_start_pos[1] - self.mouse_pos[1]
            distance = math.sqrt(dx*dx + dy*dy)
            print(f"   Drag distance: {distance:.1f}")
            print(f"   Drag vector: ({dx:.0f}, {dy:.0f})")
            
        super()._handle_mouse_up(event)
    
    def update_physics(self, dt):
        """Override to add logging."""
        self.frame_count += 1
        
        # Log every 30 frames (0.5 seconds at 60fps)
        if self.frame_count % 30 == 0:
            print(f"\n⚙️ PHYSICS UPDATE (Frame {self.frame_count})")
            for i, ball in enumerate(self.balls):
                print(f"   Ball {i}: pos=({ball.x:.0f},{ball.y:.0f}), vel=({ball.vx:.0f},{ball.vy:.0f}), state={ball.state}")
            if hasattr(self, 'birds'):
                print(f"   Birds: {len(self.birds)}")
            if hasattr(self, 'ammo_count'):
                print(f"   Ammo: {self.ammo_count}")
        
        super().update_physics(dt)
    
    def draw(self):
        """Override to add visual debugging."""
        super().draw()
        
        # Draw debug info on screen
        if self.balls:
            for i, ball in enumerate(self.balls):
                # Draw ball position text
                font = pygame.font.Font(None, 20)
                text = f"B{i}:({int(ball.x)},{int(ball.y)})"
                surface = font.render(text, True, Colors.BLACK)
                self.screen.blit(surface, (ball.x + 30, ball.y))
                
                # Draw velocity vector
                if abs(ball.vx) > 1 or abs(ball.vy) > 1:
                    end_x = ball.x + ball.vx * 0.1
                    end_y = ball.y + ball.vy * 0.1
                    pygame.draw.line(self.screen, Colors.RED, 
                                   (ball.x, ball.y), (end_x, end_y), 2)
        
        # Draw mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        font = pygame.font.Font(None, 16)
        mouse_text = f"Mouse:({mouse_x},{mouse_y})"
        mouse_surface = font.render(mouse_text, True, Colors.BLACK)
        self.screen.blit(mouse_surface, (mouse_x + 10, mouse_y - 20))
        
        pygame.display.flip()
    
    def _check_ball_out_of_bounds(self, ball: Ball) -> None:
        """Override to add logging when balls might be removed."""
        # Check if ball would be removed
        is_stationary = (ball.y + ball.radius >= self.height and 
                        abs(ball.vx) < 10 and abs(ball.vy) < 10)
        
        if is_stationary:
            print(f"\n🎾 BALL REMOVAL CHECK:")
            print(f"   Ball pos: ({ball.x:.0f},{ball.y:.0f})")
            print(f"   Ball vel: ({ball.vx:.0f},{ball.vy:.0f})")
            print(f"   Ball state: {ball.state}")
            print(f"   has_been_launched flag: {ball.has_been_launched}")
            print(f"   Max velocities: vx={ball.max_vx:.0f}, vy={ball.max_vy:.0f}")
            print(f"   Is stationary? {is_stationary}")
            print(f"   Will remove? {ball.has_been_launched and is_stationary}")
        
        # Call parent implementation
        super()._check_ball_out_of_bounds(ball)
    
    def _log_game_state(self, context=""):
        """Log complete game state."""
        print(f"\n📸 GAME STATE SNAPSHOT: {context}")
        print(f"   Balls: {len(self.balls)}")
        for i, ball in enumerate(self.balls):
            print(f"      Ball {i}: pos=({ball.x:.0f},{ball.y:.0f}), vel=({ball.vx:.0f},{ball.vy:.0f}), state={ball.state}")
            print(f"              max_vx={ball.max_vx:.0f}, max_vy={ball.max_vy:.0f}")
        print(f"   Dragging: {self.dragging_ball is not None}")
        if self.dragging_ball:
            print(f"      Dragging ball at ({self.dragging_ball.x:.0f},{self.dragging_ball.y:.0f})")
        if hasattr(self.game_state, 'ammo_count'):
            print(f"   Ammo: {self.game_state.ammo_count}")
        if hasattr(self.game_state, 'score'):
            print(f"   Score: {self.game_state.score}")

def main():
    print("\n" + "="*80)
    print("🔍 STARTING DEBUG VERSION OF BOUNCING BALL")
    print("="*80)
    print("This version will log:")
    print("  • Every mouse click and position")
    print("  • Every ball position and velocity")
    print("  • Every drag operation")
    print("  • Every physics update")
    print("  • Every collision")
    print("\nLook for:")
    print("  • 🖱️ for mouse events")
    print("  • 🎯 for targeting/grabbing")
    print("  • 🚀 for launching")
    print("  • ⚙️ for physics updates")
    print("  • 📸 for state snapshots")
    print("="*80 + "\n")
    
    try:
        game = DebugBouncingBallSimulation()
        game.run()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()