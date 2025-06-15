import React from "react";
import banner from "./default_wallpaper.jpg";
import profile from "./default_personal.jpg";
import logout_ico from "./icons8-logout-48.png";

const Header = () => {
    return (
      <>
        <header className="relative w-full h-64 md:h-48 overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent" />

            {/* Banner Image */}
            <img
                src={banner}
                alt="Banner"
                className="w-full h-full object-cover"
            />
           
        </header>
        <div className="absolute top-32  left-6">
            <img
            src={profile}
            alt="Profile"
            className="w-32 h-32 rounded-full border-4 border-white shadow-lg object-cover"
            />
        </div>
        <div className="absolute top-[150px] left-[170px] text-white">
                <h1 className="text-3xl font-bold">Mina Eissa</h1>
                <br />
                <h3 className="text-xl font-bold text-black">This is bio for user</h3>
        </div>
        
    </>
  );
};

export default Header;
