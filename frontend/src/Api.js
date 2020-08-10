import axios from "axios";
import useAsync from "./UseAsync";


export const getContests = async () => {
    const response = await axios.get("api/v1/contests/contest/");
    return response.data;
}

export const getContest = async (id) => {
    const response = await axios.get(`api/v1/contests/contest/${id}/`);
    return response.data;
}