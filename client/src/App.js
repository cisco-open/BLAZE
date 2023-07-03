
import { SummarizationPage } from './pages/summarization/Summarization';
import { SearchPage } from './pages/search/Search';
import { BenchmarkPage } from './pages/benchmark/Benchmark';
import { ComparisionPage } from './pages/benchmark/Comparision';
import { Provider } from 'react-redux';
import store from './store';
import { BasePage } from './pages/BasePage';

function App() {
  return (
    <Provider store={store}>
      <BasePage />
    </Provider>
    
  );
}

export default App;
