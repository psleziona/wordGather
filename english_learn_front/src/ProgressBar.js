import { Component } from "react";
import './ProgressBar.scss'

class ProgressBar extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        const percentageProgress = (this.props.progress * 100).toFixed(2) //%
        return (
            <div className='progress-bar'>
                <p className='progress-text'>{percentageProgress} %</p>
                <div style={{width: `${percentageProgress}%`}} className='show-progress'></div>
            </div>
        )
    }
}

export default ProgressBar;