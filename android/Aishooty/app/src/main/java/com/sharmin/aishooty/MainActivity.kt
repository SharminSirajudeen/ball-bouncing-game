package com.sharmin.aishooty

import android.graphics.Rect
import android.os.Build
import android.os.Bundle
import android.view.View
import android.view.WindowInsets
import android.view.WindowInsetsController
import android.view.WindowManager
import android.widget.FrameLayout
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import nl.dionsegijn.konfetti.KonfettiView
import nl.dionsegijn.konfetti.ParticleSystem
import nl.dionsegijn.konfetti.listeners.OnParticleSystemUpdateListener
import nl.dionsegijn.konfetti.models.Shape
import nl.dionsegijn.konfetti.models.Size

class MainActivity : AppCompatActivity() {
    private val konfettiView: KonfettiView by lazy { findViewById(R.id.konfettiView) }
    private val imageView: PlayableImageView by lazy { findViewById(R.id.playable_image_view) }
    private val swipeRefreshLayout: SwipeRefreshLayout by lazy { findViewById(R.id.swipe_refresh_layout) }


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.home_screen)
        setKonfettiView()
        setTransparentStatusBar()
    }

    private fun setKonfettiView() {
        val width = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            val windowMetrics = windowManager.currentWindowMetrics
            val insets = windowMetrics.windowInsets
                .getInsetsIgnoringVisibility(WindowInsets.Type.systemBars())
            windowMetrics.bounds.width() - insets.left - insets.right
        } else {
            @Suppress("DEPRECATION")
            resources.displayMetrics.widthPixels
        }
        konfettiView.build().apply {
            addColors(
                getColor(R.color.purple_500),
                getColor(R.color.purple_700),
                getColor(R.color.red),
                getColor(R.color.yellow),
            )
            setDirection(0.0, 359.0)
            setSpeed(1f, 5f)
            setFadeOutEnabled(true)
            setTimeToLive(50000L)
            addShapes(Shape.Square, Shape.Circle)
            addSizes(Size(10, 2f))
            setPosition(-50f, width + 50f, -50f, -50f)
            streamFor(100, 50000L)
        }
        konfettiView.onParticleSystemUpdateListener =
            object : OnParticleSystemUpdateListener {
                override fun onParticleSystemStarted(
                    view: KonfettiView,
                    system: ParticleSystem,
                    activeSystems: Int
                ) {
                }

                override fun onParticleSystemEnded(
                    view: KonfettiView,
                    system: ParticleSystem,
                    activeSystems: Int
                ) {
//                    konfettiView.visibility = View.GONE
                }
            }
    }

    override fun onDestroy() {
        super.onDestroy()
        (konfettiView.parent as? FrameLayout)?.removeView(konfettiView)
    }

    fun setTransparentStatusBar() {
        WindowCompat.setDecorFitsSystemWindows(window, false)
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            window.insetsController?.let {
                it.hide(WindowInsets.Type.statusBars())
                it.systemBarsBehavior = WindowInsetsController.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
            }
        } else {
            @Suppress("DEPRECATION")
            window.decorView.systemUiVisibility = (
                    View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                            or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                            or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                            or View.SYSTEM_UI_FLAG_FULLSCREEN
                            or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                            or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY)
        }
        
        window.statusBarColor = android.graphics.Color.TRANSPARENT
        window.navigationBarColor = android.graphics.Color.TRANSPARENT
    }

    private fun isTouchInsideView(x: Int, y: Int, view: View): Boolean {
        val rect = Rect()
        view.getGlobalVisibleRect(rect)
        return rect.contains(x, y)
    }
}