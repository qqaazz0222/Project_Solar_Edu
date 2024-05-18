import axios from "axios";

const API = "http://localhost:5174";

const getData = async (vid = "") => {
    try {
        const response = await axios.post(API + "/gen", {
            vid: vid,
        });
        return response.data;
    } catch (err) {
        console.error("요청 중 오류 발생", err);
        return { err: err };
    }
};

export { getData };
