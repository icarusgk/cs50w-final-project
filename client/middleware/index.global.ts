import type { ITag } from '@/types';

export default defineNuxtRouteMiddleware(async (to) => {
  if (to.name === 'login' || to.name === 'register') {
    const auth = useAuthStore();
    if (auth.isAuthed) {
      return { name: 'index' };
    }
  }

  if (to.name === 'tags-name') {
    const tag = to.params.name;
    const chore = useChoreStore();
    const alert = useAlertStore();

    const tags = await chore.fetchTags();

    if (!tags.find((t: ITag) => t.name === tag)) {
      alert.error(`There is no tag named ${tag}`, );
      return { name: 'tags' };
    }
  }
})