import axios from "axios";


export const getContests = async () => {
    const response = await axios.get("api/v1/contests/contest/");
    return response.data;
}

// export const getContest = async () => {
//     // const response = await axios.get(`api/v1/contests/contest/${<int:pk>}/`);
//     return response.data;
// }