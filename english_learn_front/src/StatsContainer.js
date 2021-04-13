import { Component } from "react";
import ProgressBar from './ProgressBar';

class StatsContainer extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <ul>
                <li>{this.props.word}</li>
                <li>Showed: {this.props.counter} times</li>
                <ProgressBar progress={this.props.progress} />
            </ul>
        )
    }
}

export default StatsContainer;