<template>
  <div id="login-signup">
    <router-link to="/login">Login</router-link>
    <span> or </span>
    <router-link to="/register">Sign up</router-link>
  </div>
  <div id="message">To add tasks and projects</div>
</template>
<style scoped lang="scss">
a {
  text-decoration: none;
  color: white;
  transition: color 0.2s ease-in;
}
a:hover {
  text-decoration: solid;
  color: rgb(255, 201, 201);
}
#login-signup {
  display: block;
  font-size: 2rem;
  font-weight: 600;
  padding: 1rem;
  background-color: var(--vivid-red);
  border-radius: 10px;
  margin-top: 8rem;
  width: 80%;
}

#message {
  display: block;
  padding: 1rem 0;
  font-weight: 500;
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  #login-signup {
    font-size: 1.8rem;
    width: 80%;
    margin-top: 2rem;
  }
}
</style>
