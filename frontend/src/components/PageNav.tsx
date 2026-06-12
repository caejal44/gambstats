import { Link } from "react-router-dom";

function PageNav() {
  return (
    <nav className="page-nav">
      <Link to="/">← Home</Link>
    </nav>
  );
}

export default PageNav;