import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
 
        <h1>
          MediaSpace Caption Searcher
        </h1>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          &emsp; Upload the captions file from the video you want to search!
        </p>
        {/* drag and drop file upload code: */}
        <head>
          <title>Drag and Drop File Uplaod </title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
            <meta charSet='utf-8'></meta>

         </head>
        <body>
            <div class="drop-zone">
              <span class="drop-zone__prompt">Captions File: &emsp; </span>
              <input type="file" name="myFile" class="drop-zone__input"></input>
            </div>

            <script src="./src/main.js"></script>
        </body>

        
        {/* phrase search bar code */}
        <p>
          Phrase:
        </p>
        <input type="text" 
          width={0} // this doesn't seem to change anything. How do I make the text box appearance change?
          margin={8}
        />
        <p>
        <h7>
          Answers:
        </h7>
        </p>
        
        <a
          className="App-link"
          href="https://mediaspace.illinois.edu/"
          target="_blank"
          rel="noopener noreferrer"
        >

          UIUC MediaSpace

        </a>
        
      </header>

    </div>
    
  );
}

export default App;
