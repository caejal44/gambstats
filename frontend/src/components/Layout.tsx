import PageNav from "./PageNav";

type LayoutProps = {
  children: React.ReactNode;
  showNav?: boolean;
};

function Layout({ children, showNav = true }: LayoutProps) {
  return (
    <>
      <header className="main-header">
        <div>
          <h1 className="main-header-h1">GambStats</h1>
        </div>
      </header>

      <main className="dashboard-panel">
        {children}
      </main>

       {showNav && <PageNav />}
    </>
  );
}

export default Layout;