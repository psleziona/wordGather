import { Component } from "react";
import './TestObject.scss'
import TestAnswer from './TestAnswer';

class TestObject extends Component {
    constructor(props) {
        super(props);
        this.state = {
            answerable: true
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.rightAnswer !== this.props.rightAnswer) {
            this.setState(prevState => {
                return {
                    answerable: true
                }
            })
        }
    }

    handleAnswer = answer => {
        this.setState(prevState => {
            return {
                answerable: false
            }
        })
        const isRight = answer == this.props.rightAnswer ? true : false;
        this.props.onAnswer(this.props.word, isRight);
        return isRight
    }

    render() {
        return (
            <div>
                <h4 className='guess-word'>{this.props.word}</h4>
                <ul className='answer-list'>
                    {this.props.answers.map((answer, i) => <TestAnswer
                        onAnswer={this.handleAnswer}
                        key={i} answer={answer} answerable={this.state.answerable} />)}
                </ul>
            </div>
        )
    }
}

export default TestObject;