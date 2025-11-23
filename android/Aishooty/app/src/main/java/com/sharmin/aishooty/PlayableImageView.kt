package com.sharmin.aishooty

import android.animation.ObjectAnimator
import android.content.Context
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.View
import android.view.animation.BounceInterpolator
import androidx.appcompat.widget.AppCompatImageView

class PlayableImageView(context: Context, attrs: AttributeSet) : AppCompatImageView(context, attrs) {
    private var initialX = 0f
    private var initialY = 0f
    private var lastX = 0f
    private var lastY = 0f
    private var isDragging = false
    private var screenWidth = 0
    private var screenHeight = 0

    override fun onMeasure(widthMeasureSpec: Int, heightMeasureSpec: Int) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec)
        screenWidth = context.resources.displayMetrics.widthPixels - measuredWidth
        screenHeight = context.resources.displayMetrics.heightPixels - measuredHeight
    }

    init {
        setOnTouchListener { view, event ->
            when (event.actionMasked) {
                MotionEvent.ACTION_DOWN -> {
                    isDragging = true
                    initialX = view.x
                    initialY = view.y
                    lastX = event.rawX
                    lastY = event.rawY
                }
                MotionEvent.ACTION_MOVE -> {
                    if (isDragging) {
                        val dx = event.rawX - lastX
                        val dy = event.rawY - lastY

                        val newX = (view.x + dx).coerceIn(0f, screenWidth.toFloat())
                        val newY = (view.y + dy).coerceIn(0f, screenHeight.toFloat())

                        view.x = newX
                        view.y = newY

                        lastX = event.rawX
                        lastY = event.rawY
                    }
                }
                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    isDragging = false
                    playBounceAnimation(view)
                }
            }
            true
        }
    }

    private fun playBounceAnimation(view: View) {
        val bounceAnimationX = ObjectAnimator.ofFloat(
            view,
            "translationX",
            view.translationX,
            (screenWidth - view.width).coerceAtMost(view.x.toInt()) - initialX
        )
        bounceAnimationX.interpolator = BounceInterpolator()
        bounceAnimationX.duration = 1000
        bounceAnimationX.start()

        val bounceAnimationY = ObjectAnimator.ofFloat(
            view,
            "translationY",
            view.translationY,
            (screenHeight - view.height).coerceAtMost(view.y.toInt()) - initialY
        )
        bounceAnimationY.interpolator = BounceInterpolator()
        bounceAnimationY.duration = 1000
        bounceAnimationY.start()
    }
}
