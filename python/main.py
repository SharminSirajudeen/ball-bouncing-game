#!/usr/bin/env python3
"""
Ricochet Hunter - Web Version (Pygbag Compatible)

This is the web-deployable version of the Ricochet Hunter game,
optimized for running in browsers via Pygbag/WebAssembly.

Author: AegisX
"""

import asyncio
import sys
import os

print("⏳ Loading game modules...")

# Ensure the game module can be imported
sys.path.insert(0, os.path.dirname(__file__))

print("📦 Importing Pygame...")
import pygame

print("📦 Importing game engine...")
from bouncing_ball import BouncingBallSimulation, DisplayConstants

print("✅ All modules loaded!")


class WebGameSimulation(BouncingBallSimulation):
    """Web-compatible version of the game with async support."""

    async def run_async(self) -> None:
        """Async main simulation loop for web deployment."""
        print("🎯 RICOCHET HUNTER - Make Every Shot Count! 🎯")
        print("=" * 50)
        print("📢 GAME MECHANICS:")
        print("   • Limited Ammo: Start with 3 shots - earn more by hitting birds")
        print("   • Bird Types: Brown(1pt,+1ammo), Gold(5pt,+2ammo), Red(3pt,zigzag), Blue(10pt,+3ammo,dodges)")
        print("   • Combos: Chain hits for multiplier bonuses")
        print("   • Power-ups: Collect for special abilities")
        print("   • Obstacles: Moving clouds block shots")
        print("   • Perfect Shots: Hit bird center for 2x points")
        print("   • Miss Penalty: 5 misses in a row = lose 1 ammo")
        print("📢 CONTROLS:")
        print("   • Click & Drag: Aim and shoot")
        print("   • R: Reset game  • SPACE: Pause  • ESC/Q: Quit")
        print("=" * 50)
        print("🚀 Starting game... Good luck, hunter!")

        try:
            await self._async_main_loop()
        except Exception as e:
            print(f"❌ Game error: {e}")
            raise
        finally:
            self._cleanup()

    async def _async_main_loop(self) -> None:
        """Execute the async main simulation loop for web browsers."""
        running = True
        last_time = pygame.time.get_ticks() / 1000.0

        while running:
            # Handle events
            running = self.handle_events()

            # Calculate frame delta time
            current_time = pygame.time.get_ticks() / 1000.0
            dt = current_time - last_time
            last_time = current_time

            # Update simulation
            self.update_physics(dt)

            # Update slingshot drag if active
            if self.dragging_ball:
                # Check if mouse button is still held down
                mouse_buttons = pygame.mouse.get_pressed()
                if not mouse_buttons[0]:  # Left mouse button not pressed
                    self._release_slingshot()
                else:
                    self._update_slingshot_drag()

            # Render frame
            self.draw()

            # Maintain target framerate
            self.clock.tick(DisplayConstants.TARGET_FPS)

            # Yield control to browser (CRITICAL for pygbag)
            await asyncio.sleep(0)


async def main():
    """Async main function for web deployment."""
    try:
        print("🎮 Initializing game engine...")
        print("⏳ This may take 30-60 seconds on mobile devices...")

        # Add a small delay to let the browser render loading messages
        await asyncio.sleep(0.1)

        simulation = WebGameSimulation()

        print("✅ Game engine ready!")
        print("🎯 Starting Ricochet Hunter...")

        await simulation.run_async()
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure pygame is installed: pip install pygame")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# Run the game
if __name__ == "__main__":
    asyncio.run(main())
