import axios from "axios";

const baseURL = "/api/v1"


export const getContestList = async () => {
    const response = await axios.get(`${baseURL}/contests/contest/`);
    return response.data;
}

export const getContestDetail = async (num) => {
    const response = await axios.get(`${baseURL}/contests/contest/${num}/`);
    console.log(response);
    return response.data;
}