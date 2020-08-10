// import React from "react";
// import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
// import {faCalendar, faTrophy, faUser} from "@fortawesome/free-solid-svg-icons";
// import useAsync from "../UseAsync";
// import {getContest} from "../Api";
//
//
// const ContestDetail = () => {
//     const [state, refetch] = useAsync(getContest, []);
//     const {data: contest} = state;
//
//     console.log(contest);
//
//     return (
//         <div>
//             {!contest ? <div>Error</div> :
//                 <div className="total-wrap">
//                     <main-banner>
//                         <div>실전 <span>ㅣ</span> 진행중</div>
//                         <div>
//                             <div className="title">{contest.title}</div>
//                             <div className="subtitle">간단 설명</div>
//                         </div>
//                         <div className="summary-wrap">
//                             <div className="summary">
//                                 <div className="icon-wrap">
//                                     <FontAwesomeIcon icon={faUser} className="icon"/>
//                                 </div>
//                                 <div>20팀</div>
//                             </div>
//                             <div className="summary">
//                                 <div className="icon-wrap">
//                                     <FontAwesomeIcon icon={faCalendar} className="icon"/>
//                                 </div>
//                                 <div>20팀</div>
//                             </div>
//                             <div className="summary">
//                                 <div className="icon-wrap">
//                                     <FontAwesomeIcon icon={faTrophy} className="icon"/>
//                                 </div>
//                                 <div>20팀</div>
//                             </div>
//                         </div>
//                     </main-banner>
//                 </div>
//             }
//         </div>
//     )
// }
//
// export default ContestDetail;