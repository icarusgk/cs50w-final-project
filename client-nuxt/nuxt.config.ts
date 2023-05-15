// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ["@unocss/nuxt", "@pinia/nuxt", "@pinia-plugin-persistedstate/nuxt"],
  ssr: false,
  imports: {
    dirs: ['./stores'],
  },
  components: [{ path: '~/components', pathPrefix: false }],
  devtools: {
    enabled: true
  }
});



