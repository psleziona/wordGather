import { Component } from "react";
import './TestObject.scss'

class TestObject extends Component {
    constructor(props) {
        super(props);
        this.state = {
            disabled: false,
            answersList: []
        }
    }

    // this.props = {english_word: word, false_answers: [3], right_answers:[]...}
    genAnswer = () => {
        const rightAnswer = this.props.right_answers[Math.floor(Math.random() * this.props.right_answers.length)];
        let answers = [...this.props.false_answers, rightAnswer];
        answers = answers.sort(() => Math.random() - 0.5);
        this.setState(state => {
            return {
                answersList: answers
            }
        })
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.english_word != this.props.english_word) {
            this.genAnswer();
            this.setState(state => {
                return {
                    disabled: false
                }
            })
        }
    }

    componentDidMount() {
        this.genAnswer();
    }

    handleAnswer = e => {
        this.setState(state => {
            return {
                disabled: true
            }
        });
        const choosenAnswer = e.target.innerText;
        if (this.props.right_answers.includes(choosenAnswer)) {
            e.target.style.backgroundColor = 'green';
        } else {
            e.target.style.backgroundColor = 'red';
        }
    }

    render() {
        const answersList = this.state.answersList.map((answer, index) => {
            return <li className='test__item' key={index} onClick={this.state.disabled ? undefined : this.handleAnswer}>{answer}</li>
        });

        return (
            <div className={`test_container ${this.state.disabled ? 'answered' : ''}`}>
                <h3 className='test_word'>{this.props.english_word}</h3>
                <ul className="test__list">
                    {answersList}
                </ul>
            </div>
        )
    }
}

export default TestObject;