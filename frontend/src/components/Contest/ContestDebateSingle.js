import React from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faComment, faStar, faThumbsUp} from "@fortawesome/free-regular-svg-icons";

const ContestDebateSingle = ({props}) => {
    return (
        <div className="total-wrap debate-single">
            <div className="image"><img src="" alt=""/></div>

            <div className="debate-content">
                <div className="title">{props}</div>
                <div className="subtitle">
                    글쓴이<span>ㅣ</span>2020sus 7월 10일
                </div>
            </div>

            <div className="debate-summary">
                <div className="summary-item like">
                    <FontAwesomeIcon icon={faThumbsUp}/>
                    <div>2개</div>
                </div>
                <div className="summary-item scrap">
                    <FontAwesomeIcon icon={faStar}/>
                    <div>2개</div>
                </div>
                <div className="summary-item ">
                    <FontAwesomeIcon icon={faComment}/>
                    <div>2개</div>
                </div>
            </div>
        </div>
    )
}

export default ContestDebateSingle;