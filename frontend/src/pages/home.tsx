import Navbar from "./home/components/navbar"
import Hero from "./home/components/hero"
import Feature from "./home/components/feature"
export default function Home() {
    return (
     <div className="w-full">
        <Navbar></Navbar>
        <Hero/>
        <Feature></Feature>
     </div>
    )
}