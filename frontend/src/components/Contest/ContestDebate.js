import React, {useEffect, useState} from "react";
import {getContestDebate} from "../../Api";

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


                </div>
            }
        </div>
    )
}

export default ContestDebate;