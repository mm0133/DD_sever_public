import React, {useEffect, useState} from "react";
import {getContestDebate} from "../../apis/api";
import ContestDebateSingle from "./ContestDebateSingle";

const ContestDebate = () => {
    const [debates, setDebates] = useState([]);

    useEffect(() => {
        const init = async () => {
            const data = await getContestDebate();

            setDebates(data);
        }
        init();
    }, [])

    return (
        <div>
            {!debates ? <div>없다 이자식</div> :
                <div className="total-wrap">
                    <div>
                        {debates.map(debate =>
                            <ContestDebateSingle
                                key={debate.id}

                                id={debate.id}
                                contest={debate.contest}
                                title={debate.title}
                                createdAt={debate.createdAt}

                                writerNickname={debate.writerNickname}
                                writerImage={debate.writerImage}
                                likeNums={debate.likeNums}
                                isLiked={debate.isLiked}
                                isScrape={debate.isScrape}
                                scrapNums={debate.scrapNums}
                                hitNums={debate.hitNums}
                            />
                        )}
                    </div>

                </div>
            }
        </div>
    )
}

export default ContestDebate;