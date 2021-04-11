import { Component } from "react";
import './TestAnswer.scss'

class TestAnswer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            isAnsweredRight: null
        }
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.answerable == false && this.props.answerable == true) {
            this.setState(prvState => {
                return {
                    isAnsweredRight: null
                }
            })
        }
    }

    handleClick = e => {
        const isTrue = this.props.onAnswer(e.target.innerText);
        console.log(isTrue);
        if (isTrue) {
            this.setState(prevState => {
                return {
                    isAnsweredRight: true
                }
            })
        } else {
            this.setState(prevState => {
                return {
                    isAnsweredRight: false
                }
            })
        }
    }

    render() {
        const answerable = this.props.answerable;
        let bgClass = '';
        if (this.state.isAnsweredRight) {
            bgClass = 'right';
        } else if (this.state.isAnsweredRight == false) {
            bgClass = 'wrong';
        }
        return (
            <li className={`list-item ${bgClass}`}
                onClick={answerable ? this.handleClick : null}>{this.props.answer}</li>
        )
    }
}

export default TestAnswer;