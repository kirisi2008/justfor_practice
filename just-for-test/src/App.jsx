import React from "react";
import logo from "./logo.svg";
import "./App.css";
import { Row, Col } from "antd"
import { simpleBox } from "./boxModules/SimpleBox"

const App = () => (
  <div className="App">
    {/* <header className="App-header"> */}

    <div>
      <Row>
        <Col span={8}>col-8</Col>
        <Col span={8} offset={8}>
          col-8
      </Col>
      </Row>
      <Row>
        <Col span={6} offset={6}>
          col-6 col-offset-6
      </Col>
        <Col span={6} offset={6}>
          col-6 col-offset-6
      </Col>
      </Row>
      <Row>
        <Col span={12} offset={6}>
          col-12 col-offset-6
      </Col>
      </Row>
    </div>
    <div>
      {simpleBox}
    </div>
    {/* <a
        className="App-link"
        href="https://reactjs.org"
        target="_blank"
        rel="noopener noreferrer"
      >
        Learn React
			</a> */}
    {/* </header> */}
    {/* <TodoApp /> */}
  </div>
);

const TodoApp = ({ items, text }) => {
  const handleChange = (e) => {
    this.setState({ text: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!this.state.text.length) {
      return;
    }
    const newItem = {
      text: this.state.text,
      id: Date.now()
    };
    this.setState(state => ({
      items: state.items.concat(newItem),
      text: ""
    }));
  };
};

// class TodoApp extends React.Component {
//   constructor(props) {
//     super(props);
//     this.state = { items: [], text: "" };
//     this.handleChange = this.handleChange.bind(this);
//     this.handleSubmit = this.handleSubmit.bind(this);
//   }

//   render() {
//     return (
//       <div>
//         <h3>TODO</h3>
//         <TodoList items={this.state.items} />
//         <form onSubmit={this.handleSubmit}>
//           <label htmlFor="new-todo">
//             What needs to be done?
// 					</label>
//           <input
//             id="new-todo"
//             onChange={this.handleChange}
//             value={this.state.text}
//           />
//           <button>
//             Add #{this.state.items.length + 1}
//           </button>
//         </form>
//       </div>
//     );
//   }

//   handleChange(e) {

//   }

//   handleSubmit(e) {

//   }
// }

// class TodoList extends React.Component {
//   render() {
//     return (
//       <ul>
//         {this.props.items.map(item => (
//           <li key={item.id}>{item.text}</li>
//         ))}
//       </ul>
//     );
//   }
// }

export default App;
