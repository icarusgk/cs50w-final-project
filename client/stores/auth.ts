import type { IUser } from '@/types';

type UserCredentials = {
  username: string;
  password: string;
  passwordConfirmation?: string;
};

export const useAuthStore = defineStore('auth', () => {
  const user = ref<IUser | null>(null);
  const isAuthed = ref(false);
  const error = ref();
  const alerts = useAlertStore();
  const router = useRouter();

  // First is login in, this will not have an error
  async function login(credentials: UserCredentials) {
    try {
      const { status } = await useRawFetch('auth/login/', { method: 'POST', body: credentials });
      if (status === 200) {
        // After the user logs in, we get its user
        await getUser();
        error.value = null;
        alerts.success('Successfully logged in!');
        // And we push the user to the main / page
        await router.push('/');
      }
    } catch (e: any) {
      error.value = e;
    }
  }

  // Runs at start
  async function getUser() {
    try {
      const { _data, status } = await useRawFetch<IUser>('me/');

      if (status === 200 && _data) {
        user.value = _data;
        isAuthed.value = true;
      } else {
        isAuthed.value = false;
      }
    } catch (e) {
      // If refresh token is not longer valid, logout
      logout();
    }
  }

  async function register(credentials: UserCredentials) {
    error.value = null;
    try {
      const response = await useRawFetch('auth/register/', {
        method: 'post',
        body: { credentials }
      });
      if (response.status === 201) {
        // If the user is created, log him in
        login({
          username: credentials.username,
          password: credentials.password,
        });
      }
    } catch (err: any) {
      error.value = err;
    }
    router.push('/register');
  }

  async function logout() {
    if (!isAuthed.value) return;

    const response = await useRawFetch('auth/logout/', { method: 'post' });

    if (response.status === 200) {
      // Reset user state
      user.value = null;
      isAuthed.value = false;

      alerts.info('Logged out!');
      localStorage.clear();

      await router.push('/');
    }
  }

  return { user, isAuthed, error, login, getUser, register, logout }
},
{ persist: true });
