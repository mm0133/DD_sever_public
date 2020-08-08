import React, {useState, useEffect} from "react";
import axios from "axios";
import ContestSingle from "../components/ContestSingle";

const ContestList = () => {
    const [contests, setContest] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchContests = async () => {
            try {
                setContest(null);
                setError(null);
                setLoading(true);

                const response = await axios.get("api/v1/contests/contest/");
                setContest(response.data);
            } catch (e) {
                setError(e);
            }
            setLoading(false);
        }
        fetchContests();
    }, [])

    if (loading) return <div>"로딩중입니다"</div>
    if (error) return <div>에러가 발생했습니다.</div>
    if (!contests) return null;

    return (
        <div>
            {contests.map(contest =>
                <ContestSingle
                    key={contest.id}
                    title={contest.title}
                    createdAt={contest.createdAt}
                    updatedAt={contest.updatedAt}
                    deadline={contest.deadline}
                    profileThumb={contest.profileThumb}
                    timeline={contest.timeline}
                    prize={contest.prize}
                    isForTraining={contest.isForTraining}
                    difficulty={contest.difficulty}
                    evaluationMethod={contest.evaluationMethod}
                    learningModel={contest.learningModel}

                    isScrapped={contest.isScrapped}
                    scrapNums={contest.scrapNums}
                    isFinished={contest.isFinished}
                />)
            }
        </div>
    );
};

export default ContestList;