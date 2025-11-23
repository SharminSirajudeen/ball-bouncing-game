package com.example.bouncingball.view

import android.content.Context
import android.graphics.*
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import androidx.core.content.ContextCompat
import com.example.bouncingball.R
import com.example.bouncingball.physics.PhysicsWorld
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.TimeUnit

class BallGameView @JvmOverloads constructor(
    context: Context,
    attrs: AttributeSet? = null,
    defStyleAttr: Int = 0
) : View(context, attrs, defStyleAttr) {

    private var physicsWorld: PhysicsWorld? = null
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val shadowPaint = Paint(Paint.ANTI_ALIAS_FLAG)
    
    private var ballColor = ContextCompat.getColor(context, R.color.ball_default)
    private var backgroundColor = ContextCompat.getColor(context, R.color.background)
    
    private var executor: ScheduledExecutorService? = null
    private val timeStep = 1f / 60f // 60 FPS
    
    private val ballGradient = RadialGradient(
        0f, 0f, 1f,
        intArrayOf(Color.WHITE, ballColor, darkenColor(ballColor)),
        floatArrayOf(0f, 0.7f, 1f),
        Shader.TileMode.CLAMP
    )

    init {
        setupPaints()
    }

    private fun setupPaints() {
        paint.apply {
            style = Paint.Style.FILL
            shader = ballGradient
        }
        
        shadowPaint.apply {
            style = Paint.Style.FILL
            color = Color.BLACK
            alpha = 50
            maskFilter = BlurMaskFilter(20f, BlurMaskFilter.Blur.NORMAL)
        }
        
        // Enable hardware acceleration for better performance
        setLayerType(LAYER_TYPE_HARDWARE, null)
    }

    override fun onSizeChanged(w: Int, h: Int, oldw: Int, oldh: Int) {
        super.onSizeChanged(w, h, oldw, oldh)
        
        // Initialize physics world with screen dimensions
        physicsWorld?.destroy()
        physicsWorld = PhysicsWorld(w.toFloat(), h.toFloat())
        
        // Update gradient with proper ball size
        updateBallGradient()
        
        // Start physics simulation
        startSimulation()
    }

    private fun updateBallGradient() {
        val radius = physicsWorld?.getBallRadius() ?: 50f
        paint.shader = RadialGradient(
            0f, 0f, radius,
            intArrayOf(
                adjustAlpha(Color.WHITE, 200),
                ballColor,
                darkenColor(ballColor)
            ),
            floatArrayOf(0f, 0.6f, 1f),
            Shader.TileMode.CLAMP
        )
    }

    private fun startSimulation() {
        stopSimulation()
        
        executor = Executors.newSingleThreadScheduledExecutor()
        executor?.scheduleAtFixedRate({
            physicsWorld?.step(timeStep)
            postInvalidate()
        }, 0, (timeStep * 1000).toLong(), TimeUnit.MILLISECONDS)
    }

    private fun stopSimulation() {
        executor?.shutdown()
        executor = null
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        
        // Draw background
        canvas.drawColor(backgroundColor)
        
        physicsWorld?.let { world ->
            val (x, y) = world.getBallPosition()
            val radius = world.getBallRadius()
            
            // Draw shadow
            canvas.save()
            canvas.translate(x + 5, y + 5)
            canvas.drawCircle(0f, 0f, radius, shadowPaint)
            canvas.restore()
            
            // Draw ball with gradient
            canvas.save()
            canvas.translate(x, y)
            canvas.drawCircle(0f, 0f, radius, paint)
            
            // Add highlight for 3D effect
            val highlightPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                style = Paint.Style.FILL
                shader = RadialGradient(
                    -radius * 0.3f, -radius * 0.3f, radius * 0.5f,
                    intArrayOf(
                        adjustAlpha(Color.WHITE, 150),
                        adjustAlpha(Color.WHITE, 0)
                    ),
                    null,
                    Shader.TileMode.CLAMP
                )
            }
            canvas.drawCircle(0f, 0f, radius, highlightPaint)
            canvas.restore()
        }
    }

    override fun onTouchEvent(event: MotionEvent): Boolean {
        when (event.action) {
            MotionEvent.ACTION_DOWN, MotionEvent.ACTION_MOVE -> {
                physicsWorld?.applyImpulse(event.x, event.y)
                return true
            }
        }
        return super.onTouchEvent(event)
    }

    fun setBallColor(color: Int) {
        ballColor = color
        updateBallGradient()
        invalidate()
    }

    fun getBallColor(): Int = ballColor

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        stopSimulation()
        physicsWorld?.destroy()
    }

    private fun darkenColor(color: Int): Int {
        val factor = 0.7f
        val r = (Color.red(color) * factor).toInt()
        val g = (Color.green(color) * factor).toInt()
        val b = (Color.blue(color) * factor).toInt()
        return Color.rgb(r, g, b)
    }

    private fun adjustAlpha(color: Int, alpha: Int): Int {
        return Color.argb(alpha, Color.red(color), Color.green(color), Color.blue(color))
    }
}