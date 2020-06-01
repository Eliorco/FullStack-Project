<template>
<div id="login">
<h1>The Best Mail Service IN THE WORLD</h1>
<hr><br><br>
<p>Log to start sending messages to your family and friends</p>
<br>
<span v-if="loggedin">
    <button type="button" class="btn btn-success btn-sm" v-on:click="logout()">
              Logout
          </button>
  </span>

<span v-else>
    <button type="button" class="btn btn-success btn-sm" v-b-modal.login-modal>Login
          </button>
    </span>

    <b-modal ref="loginModal"
            id="login-modal"
            title="Login"
            hide-footer>
      <b-form @submit="onSubmit" class="w-100">
        <b-form-group id="form-email-group"
                    label="Enter Email:"
                    label-for="form-email-input">
          <b-form-input id="form-email-input"
                        type="text"
                        v-model="loginForm.email"
                        required
                        placeholder="try DonaldTrump@gmail.com">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-password-group"
                      label="Enter your password:"
                      label-for="form-password-input">
            <b-form-input id="form-password-input"
                          type="password"
                          v-model="loginForm.password"
                          required
                          placeholder="try blabla123">
            </b-form-input>
            <br>
            <b-button-group>
              <b-button type="submit" variant="primary">Submit</b-button>
              </b-button-group>
        </b-form-group>
      </b-form>
      </b-modal>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Login',
  data() {
    return {
      loggedin: false,
      msg: 'Hello from vue Login',
      loginForm: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();

      const payload = {
        email: this.loginForm.email,
        password: this.loginForm.password,
      };
      this.login(payload);
    },
    login(payload) {
      const path = 'http://localhost:5000/login';
      axios.post(path, payload)
        .then((res) => {
          localStorage.setItem('utoken', res.data.token);
          this.$router.push('Messages');
          this.msg = res.data;
          this.loggedin = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    logout() {
      this.token = '';
    },
  },
};
</script>
