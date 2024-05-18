import { create } from "zustand";

const newTodoStore = (set) => ({
    newTodoData: {
        name: "",
        type: "",
        sDate: new Date(),
        eDate: new Date(),
        detail: "",
    },
    setNewTodo: (value) =>
        set(() => ({
            newTodoData: value,
        })),
    clearNewTodo: () =>
        set({
            newTodoData: {
                name: "",
                type: "",
                sDate: new Date(),
                eDate: new Date(),
                detail: "",
            },
        }),
});

const useNewTodoStore = create(newTodoStore);

export { useNewTodoStore };
