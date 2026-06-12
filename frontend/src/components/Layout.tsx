import PageNav from "./PageNav";

type LayoutProps = {
  children: React.ReactNode;
};

function Layout({ children }: LayoutProps) {
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

       <PageNav />
    </>
  );
}

export default Layout;