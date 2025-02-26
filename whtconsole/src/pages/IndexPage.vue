<template>
  <q-page class="splash-page">
    <div class="splash-overlay">
      <div class="content-container">
        <h1 class="text-h2 text-white q-mb-xl text-center">
          {{ $t('splash.title') }}
        </h1>
        <p class="text-h5 text-white q-mb-xl text-center">
          {{ $t('splash.subtitle') }}
        </p>
        <q-btn
          class="start-button"
          color="white"
          text-color="primary"
          :label="$t('splash.startButton')"
          size="lg"
          to="/admin"
          unelevated
          rounded
        >
          <q-ripple />
        </q-btn>
      </div>
      <div class="credits">
        Made with <q-icon name="auto_awesome" color="red-5" /> by <a href="https://github.com/imnaoj" target="_blank" class="joan">Joan</a> using 
        <span class="cursor">Cursor</span> + <span class="claude">Claude</span>
      </div>
    </div>
  </q-page>
</template>

<script>
import { onMounted } from 'vue'

// Predefined color pairs that work well together
const colorPairs = [
  ['#2193b0', '#6dd5ed'], // Blue Gradient
  ['#cc2b5e', '#753a88'], // Purple Love
  ['#42275a', '#734b6d'], // Mauve
  ['#de6262', '#ffb88c'], // Red Sunset
  ['#06beb6', '#48b1bf'], // Aqua Marine
  ['#614385', '#516395'], // Deep Purple
  ['#02aab0', '#00cdac'], // Green Beach
  ['#000428', '#004e92'], // Frost
  ['#23074d', '#cc5333'], // Sunset Vibes
  ['#1a2a6c', '#b21f1f'], // Superman
  ['#0f0c29', '#302b63'], // Stellar
  ['#360033', '#0b8793'], // Twilight
  ['#4b6cb7', '#182848'], // Deep Space
  ['#3494e6', '#ec6ead'], // Rose Colored Lenses
  ['#283c86', '#45a247']  // Forest Blues
]

export default {
  name: 'IndexPage',
  setup() {
    const getRandomGradient = () => {
      const pair = colorPairs[Math.floor(Math.random() * colorPairs.length)]
      const angle = Math.floor(Math.random() * 360) // Random angle for gradient
      return `linear-gradient(${angle}deg, ${pair[0]}, ${pair[1]})`
    }

    onMounted(() => {
      document.querySelector('.splash-page').style.background = getRandomGradient()
    })
  }
}
</script>

<style lang="scss">
.splash-page {
  min-height: 100vh;
  background-size: cover;
  background-position: center;
  position: relative;
  transition: background 1.5s ease-in-out;

  .splash-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.2); // Lighter overlay since we have good contrast
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(3px); // Subtle blur effect
  }

  .content-container {
    text-align: center;
    padding: 2rem;
    animation: fadeIn 1.5s ease-in;

    h1, p {
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
  }

  .start-button {
    font-size: 1.2rem;
    padding: 12px 36px;
    transition: all 0.3s ease;
    border: 2px solid transparent;

    &:hover {
      transform: scale(1.05);
      border: 2px solid rgba(255, 255, 255, 0.5);
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
  }

  .credits {
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    color: white;
    font-size: 0.9rem;
    text-align: center;
    opacity: 0.8;
    transition: opacity 0.3s ease;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
    display: flex;
    align-items: center;
    gap: 4px;

    &:hover {
      opacity: 1;
    }

    .q-icon {
      font-size: 1.1rem;
      animation: heartbeat 1.5s ease-in-out infinite;
    }

    .cursor, .claude, .joan {
      text-decoration: none;
      font-weight: 700;
      color: #eeDCe2;
    }

  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes heartbeat {
  0% {
    transform: scale(1);
  }
  14% {
    transform: scale(1.3);
  }
  28% {
    transform: scale(1);
  }
  42% {
    transform: scale(1.3);
  }
  70% {
    transform: scale(1);
  }
}
</style>
