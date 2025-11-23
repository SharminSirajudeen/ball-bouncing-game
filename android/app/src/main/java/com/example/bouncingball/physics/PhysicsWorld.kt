package com.example.bouncingball.physics

import org.jbox2d.collision.shapes.CircleShape
import org.jbox2d.collision.shapes.PolygonShape
import org.jbox2d.common.Vec2
import org.jbox2d.dynamics.*

class PhysicsWorld(private val screenWidth: Float, private val screenHeight: Float) {
    companion object {
        const val WORLD_TO_SCREEN = 100f // 1 meter = 100 pixels
        const val SCREEN_TO_WORLD = 1f / WORLD_TO_SCREEN
        const val BALL_RADIUS = 0.5f // 0.5 meters
        const val RESTITUTION = 0.8f // Bounciness
        const val FRICTION = 0.3f
        const val DENSITY = 1.0f
    }

    private val world: World
    private var ballBody: Body? = null
    private val worldWidth = screenWidth * SCREEN_TO_WORLD
    private val worldHeight = screenHeight * SCREEN_TO_WORLD

    init {
        // Create Box2D world with gravity
        val gravity = Vec2(0f, 10f) // Positive Y is down
        world = World(gravity)
        
        createBoundaries()
        createBall()
    }

    private fun createBoundaries() {
        // Create static bodies for screen boundaries
        val bodyDef = BodyDef().apply {
            type = BodyType.STATIC
        }

        // Ground (bottom)
        val groundBody = world.createBody(bodyDef)
        val groundBox = PolygonShape().apply {
            setAsBox(worldWidth / 2, 0.1f, Vec2(worldWidth / 2, worldHeight), 0f)
        }
        groundBody.createFixture(groundBox, 0f).apply {
            restitution = RESTITUTION
            friction = FRICTION
        }

        // Ceiling (top)
        val ceilingBody = world.createBody(bodyDef)
        val ceilingBox = PolygonShape().apply {
            setAsBox(worldWidth / 2, 0.1f, Vec2(worldWidth / 2, 0f), 0f)
        }
        ceilingBody.createFixture(ceilingBox, 0f).apply {
            restitution = RESTITUTION
            friction = FRICTION
        }

        // Left wall
        val leftWallBody = world.createBody(bodyDef)
        val leftWallBox = PolygonShape().apply {
            setAsBox(0.1f, worldHeight / 2, Vec2(0f, worldHeight / 2), 0f)
        }
        leftWallBody.createFixture(leftWallBox, 0f).apply {
            restitution = RESTITUTION
            friction = FRICTION
        }

        // Right wall
        val rightWallBody = world.createBody(bodyDef)
        val rightWallBox = PolygonShape().apply {
            setAsBox(0.1f, worldHeight / 2, Vec2(worldWidth, worldHeight / 2), 0f)
        }
        rightWallBody.createFixture(rightWallBox, 0f).apply {
            restitution = RESTITUTION
            friction = FRICTION
        }
    }

    private fun createBall() {
        // Create dynamic body for the ball
        val bodyDef = BodyDef().apply {
            type = BodyType.DYNAMIC
            position.set(worldWidth / 2, worldHeight / 2)
            linearDamping = 0.1f // Slight air resistance
            angularDamping = 0.1f
        }

        ballBody = world.createBody(bodyDef)

        // Create circle shape for the ball
        val circleShape = CircleShape().apply {
            radius = BALL_RADIUS
        }

        // Create fixture
        val fixtureDef = FixtureDef().apply {
            shape = circleShape
            density = DENSITY
            friction = FRICTION
            restitution = RESTITUTION
        }

        ballBody?.createFixture(fixtureDef)
        
        // Give initial velocity
        ballBody?.linearVelocity = Vec2(2f, -3f)
    }

    fun step(timeStep: Float) {
        world.step(timeStep, 6, 2)
    }

    fun applyImpulse(screenX: Float, screenY: Float) {
        ballBody?.let { ball ->
            val ballPos = ball.position
            
            // Convert screen coordinates to world coordinates
            val worldX = screenX * SCREEN_TO_WORLD
            val worldY = screenY * SCREEN_TO_WORLD
            
            // Calculate impulse direction
            val impulseX = (worldX - ballPos.x) * 2f
            val impulseY = (worldY - ballPos.y) * 2f
            
            // Apply impulse
            ball.applyLinearImpulse(Vec2(impulseX, impulseY), ball.worldCenter)
        }
    }

    fun getBallPosition(): Pair<Float, Float> {
        return ballBody?.let { ball ->
            val pos = ball.position
            Pair(pos.x * WORLD_TO_SCREEN, pos.y * WORLD_TO_SCREEN)
        } ?: Pair(screenWidth / 2, screenHeight / 2)
    }

    fun getBallRadius(): Float = BALL_RADIUS * WORLD_TO_SCREEN

    fun destroy() {
        ballBody?.let { world.destroyBody(it) }
    }
}