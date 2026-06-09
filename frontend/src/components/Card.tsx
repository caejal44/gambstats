type CardProps = {
    title: string;
    text: string;
    buttonText: string;
};

function Card({ title, text, buttonText }: CardProps) {
    return (
        <div className="card">
            <div className="card-body">
                <h3 className="card-title">{title}</h3>
                <p className="card-text">{text}</p>
                <button className="card-btn">{buttonText}</button>
            </div>
        </div>
    );
}

export default Card;