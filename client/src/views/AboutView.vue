<template>
  <div class="about">
    <div class="title">
      <AboutIcon />
      <h1>About</h1>
    </div>
  </div>
  <div class="container">
    <div class="main-info">
      <div class="info">
        <div class="image">
          <div class="image-and-title">
            <img src="@/assets/tomato.png" alt="">
            <p><b>Pomodoro</b></p>
            <span>is the italian word for tomato</span>
          </div>
        </div>
        <div class="meaning">
          <h2>The Pomodoro Technique</h2>
          <p>Pomodoro is a time management method where we divide the tasks we need to do into small sections of time with regular, brief breaks to encourage sustained focus and prevent mental weariness.</p>
        </div>
      </div>
      <div class="steps-container">
        <div class="heading">
          <span class="question">How to use this technique?</span>
          <p>This technique was developed in the late 1980 by Francesco Cirillio, he described its bigges strength is its simplicity:</p>
        </div>
        <div class="steps">

          <div class="step-container">
            <span class="title">Step 1</span>
            <span class="step-body">Pick a task to be done</span>
          </div>

          <div class="step-container">
            <span class="title">Step 2</span>
            <span class="step-body">Start the Pomodoro Timer and focus on a single task until the timer rings</span>
          </div>

          <div class="step-container">
            <span class="title">Step 3</span>
            <span class="step-body">When the timer is up, reflect on what you have completed</span>
          </div>

          <div class="step-container">
            <span class="title">Step 4</span>
            <span class="step-body">Take a 5 minute break</span>
          </div>

          <div class="step-container">
            <span class="title">Step 5</span>
            <span class="step-body">Every 4 pomodoros, take a longer 15 minute break</span>
          </div>

        </div>
      </div>
    </div>
    <div class="try-list">
      <span class="desc">Try this technique if you:</span>
      <ul>
        <li>
          <span>👀</span>
          <p>Find little distractions that often derail the whole workday.</p>
        </li>
        <li>
          <span>😮‍💨</span>
          <p>Consistently work past the point of optimal productivity.</p>
        </li>
        <li>
          <span>🎯</span>
          <p>Enjoy gamified goal-setting.</p>
        </li>
        <li>
          <span>📚</span>
          <p>Have lots of open-ended work that could take unlimited amounts of time (e.g., studying for an exam, research for a blog post, etc.).</p>
        </li>
        <li>
          <span>😅</span>
          <p>Are overly optimistic when it comes to how much you can get done in a day</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped lang="scss">
.about {
  color: white;
  margin: 2rem 4rem;

  .title {
    display: flex;
    align-items: center;
    margin-left: -0.5rem;
    margin-bottom: 1rem;
    h1 {
      margin-left: 1rem;
    }
  }
}

.container {
  display: flex;
  gap: 12rem;
  color: white;
  justify-content: center;
  align-items: center;
  margin: 0 4rem;
  
  .main-info {
    
    .info {
      display: flex;

      .image {
        .image-and-title {
          text-align: center;

          img {
            padding-bottom: 1rem;
          }
        }
      }      

      .meaning {
        width: 600px;
        padding-left: 3rem;
        p {
          margin-top: 1rem;
        }
      }
    }
    .steps-container {
      padding-top: 2rem;
      .heading {
        margin-bottom: 3rem;
        .question {
          display: block;
          font-size: 1.3rem;
          font-weight: 700;
        }
      }
      .steps {
        width: 950px;
        display: flex;
        margin-top: 1rem;
        text-align: center;
          
        .step-container {
          display: flex;
          flex-direction: column;
          margin-right: 2rem;
          
          .title {
            display: block;
            font-weight: 600;
            margin-left: 0.05rem;
            margin-bottom: 1rem;
          }
        }
      }
    }
  }
  .try-list {
    width: 20%;
    .desc {
      display: block;
      font-size: 1.2rem;
      font-weight: 600;
    }
    ul {
      list-style: none;
      li {
        display: flex;
        margin-top: 1rem;
        span {
          padding-right: 0.75rem;
        }
      }
    }
  }
}

@media (max-width: 1600px) {
  .container {
    flex-direction: column;
    margin: 0 2rem;
    gap: 2rem;

    .main-info {
      width: 80%;
      justify-content: center;
    }
    
    .try-list {
      margin: 4rem 0;
      width: 70%;
    }
  }  
}

@media (max-width: 1400px) {
  .container {
    flex-direction: column;
    margin: 0 rem;
    gap: 2rem;

    .try-list {
      width: 80%;
    }
  }
}

@media (max-width: 1100px) {
  .container {
    .main-info {
      width: 85%;
      .steps-container {
        margin: 0;
        .steps {
          flex-direction: column;
          width: 100%;
          margin-top: 2rem;
          .step-container {
            margin-bottom: 1rem;
            .title {
              display: block;
              font-weight: 600;
              margin: 0;
            }
          }
        }
      }
    }
    .try-list {
      margin-top: 0;
      margin-bottom: 2rem;
    }
  }
}

@media (max-width: 768px) {
  .about {
    margin: 1rem;
  }
  .container {
    flex-direction: column;
    .main-info {
      width: 100%;
      .info {
        flex-direction: column;
        .meaning {
          margin-top: 3rem;
          padding: 0;
          width: 100%;
          text-align: center;
        }
      }
      .steps-container {
        text-align: center;
      }
    }
    .try-list {
      width: 100%;
    }
  }
}
</style>
