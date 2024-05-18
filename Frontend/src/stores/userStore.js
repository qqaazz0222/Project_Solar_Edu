import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";

const userStore = (set) => ({
    userData: {
        uid: "",
        name: "",
        token: "",
    },
    setUser: (value) =>
        set(() => ({
            userData: value,
        })),
    clearUser: () => set({ userData: { uid: "", name: "", token: "" } }),
});

const useUserStore = persist(userStore, {
    name: "userStore",
    storage: createJSONStorage(() => sessionStorage),
});

export default create(useUserStore);
