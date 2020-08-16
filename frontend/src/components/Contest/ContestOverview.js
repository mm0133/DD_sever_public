import React, {useState} from "react";
import "./ContestOverview.scss"

const ContestOverview = (props) => {
    const [title, setTitle] = useState("개요");
    const [contents, setContents] = useState(`${props.contestExplanation}`);

    const getSummary = () => {
        setTitle("개요");
        setContents(props.contestExplanation);
    }

    const getPrize = () => {
        setTitle("상금");
        setContents(props.prizeExplanation);
    }

    const getEvaluation = () => {
        setTitle("규칙");
        setContents(props.evaluationExplanation);
    }

    return (
        <div className="total-wrap overview">
            <timeline>

            </timeline>

            <div className="main-content">
                <menu>
                    <div className="title">메뉴</div>
                    <div className="menu">
                        <div><button className="menu-item" onClick={getSummary}>개요</button></div>
                        <div><button className="menu-item" onClick={getPrize}>상금</button></div>
                        <div><button className="menu-item" onClick={getEvaluation}>규칙</button></div>
                    </div>
                </menu>
                <contents>
                    <div className="title">{title}</div>
                    <div className="contents">{contents}</div>
                </contents>
            </div>
        </div>
    )
}

export default ContestOverview;