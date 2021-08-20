import Dropdown from 'react-bootstrap/Dropdown';

function SettingsTab() {
  const container = {
    margin: "4rem 0 0 0"
  };
  const feature = {
    margin: "5rem auto",
    width: "70%",
    padding: "3rem 3rem",
    backgroundColor: '#fbc31c',
  };
  const dropdown = {
    backgroundColor: '#4992bb',
  };
  function changeLanguage() {
    localStorage.setItem('language', '/en-ie')
  };
  return(
    <div style={container}>
      <div style={feature}>
        <h3>Roghnaigh Teanga:</h3>
        <p>Roghnaigh idir Béarla nó Gaeilge</p>
        <Dropdown>
          <Dropdown.Toggle id="dropdown-button-dark-example1" variant="secondary" style={dropdown}>
            Teanga
          </Dropdown.Toggle>

          <Dropdown.Menu variant="dark" style={dropdown}>
            <Dropdown.Item onClick={changeLanguage()} href="/en-ie">English</Dropdown.Item>
            <Dropdown.Item active>Gaeilge</Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      </div>
      <div style={feature}>
        <h3>Shuiteáil an aip:</h3>
        <p>Don feidhmiú agus inrochtaineacht is fearr molaimid duit an aip a suiteáil ar do gléas.</p>
        <p>Le haigh sé seo a bheith indéanta is aip gréasáin forásach í an aip seo. Teigh go dtí socruite do brabhsálaí gréasáin agus cliceáil ar an rogha "Install Best Bus".</p>
        <p>Faroar níl an gné seo ar fáil ar gach gléas no brabhsálaí gréasáin.</p>
      </div>
    </div>

  )
}

export default SettingsTab;