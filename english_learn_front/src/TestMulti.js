import { Component } from "react";

class TestMulti extends Component {
    constructor() {
        super();
        this.state = {
            countValue: '5',
            testArray: []
        }
    }

    generateTest = () => {
        
    }

    getData = count => {
        fetch(`/words/${count}`)
        .then(res => res.json())
        .then(data => {
            this.setState(state => {
                return {
                    testArray: data
                }
            })
        })
    }

    handleChange = e => {
        this.setState(state => {
            return {
                countValue: e.target.value
            }
        });
    }

    handleClick = e => {
        this.getData(this.state.countValue);
    }


    render() {
        const testEl = this.state.testArray.map((tObj, i) => {
            const { english_word, false_answers, right_answers } = tObj;
            return <TestObject key={i} english_word={english_word} false_answers={false_answers} right_answers={right_answers} />
        });

        return (
            <div>
                <select value={this.state.countValue} onChange={this.handleChange}>
                    <option value='5'>5</option>
                    <option value='10'>10</option>
                    <option value='20'>20</option>
                </select>
                <button onClick={this.handleClick}>Pobierz</button>
                {testEl}
            </div>
        )
    }
}

export default TestMulti;

class TestObject extends Component {
    constructor(props) {
        super(props);
    }

    genAnswer = () => {
        const rightAnswer = this.props.right_answers[Math.floor(Math.random() * this.props.right_answers.length)];
        let answers = [...this.props.false_answers, rightAnswer];
        answers = answers.sort(() => {
            let a = Math.random() - 0.5;
            console.log(a);
            return a;
        });
        console.log(answers)
    }

    render() {
        console.log(this.props)
        return (
            <div className='test_container'>
                <button onClick={this.genAnswer}>Klik</button>
            </div>
        )
    }
}