import { Link } from "react-router-dom";

type CardProps = {
  title: string;
  text: string;
  buttonText: string;
  path?: string;
};

function Card({ title, text, buttonText, path }: CardProps) {
  return (
    <div className="card">
      <div className="card-body">
        <h3 className="card-title">{title}</h3>
        <p className="card-text">{text}</p>

        {path ? (
          <Link className="card-btn" to={path}>
            {buttonText}
          </Link>
        ) : (
          <button className="card-btn">{buttonText}</button>
        )}
      </div>
    </div>
  );
}

export default Card;