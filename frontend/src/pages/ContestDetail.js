import React from "react";

const ContestDetail = ({match}) => {
    return (
        <div>
            <div>디테일</div>
            <div>{match.params.id}</div>
        </div>
    )
}

export default ContestDetail;