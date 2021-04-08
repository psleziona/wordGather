import { Component } from "react";
import TestObject from './TestObject';

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