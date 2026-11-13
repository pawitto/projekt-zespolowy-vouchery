// Prototyp katalogu WWW. Dane i zakup nie sa polaczone z backendem.
class SklepVoucherow {
    constructor() {
        this.oferty = [
            { id: 1, partner: "A", partnerNazwa: "Masaże", nazwa: "Masaż relaksacyjny", cena: 180, limitUzyc: 1, kody: 1, opis: "Jedna realizacja, ważność 90 dni." },
            { id: 2, partner: "B", partnerNazwa: "Fitness", nazwa: "Karnet 10 wejść", cena: 220, limitUzyc: 10, kody: 1, opis: "Jeden kod z limitem dziesięciu wejść." },
            { id: 3, partner: "C", partnerNazwa: "Hotel", nazwa: "Weekendowy nocleg", cena: 540, limitUzyc: 1, kody: 1, opis: "Voucher na usługę hotelową." },
            { id: 4, partner: "pakiet", partnerNazwa: "Pakiet A/B/C", nazwa: "Pobyt + masaż + trening", cena: 800, limitUzyc: 1, kody: 3, opis: "Jedna transakcja, trzy osobne kody." }
        ];
        this.wybranaOferta = null;
        this.numerZakupu = 0;
        this.listaOfert = document.getElementById("listaOfert");
        this.filtrPartnera = document.getElementById("filtrPartnera");
        this.formularzZakupu = document.getElementById("formularzZakupu");
        this.filtrPartnera.addEventListener("change", () => this.pokazOferty());
        this.formularzZakupu.addEventListener("submit", (zdarzenie) => this.potwierdzZakup(zdarzenie));
        document.getElementById("anulujZakup").addEventListener("click", () => this.wrocDoOfert());
        document.getElementById("nowyZakup").addEventListener("click", () => this.wrocDoOfert());
        this.pokazOferty();
    }

    pokazOferty() {
        const filtr = this.filtrPartnera.value;
        this.listaOfert.replaceChildren();
        this.oferty.filter((oferta) => filtr === "wszyscy" || oferta.partner === filtr)
            .forEach((oferta) => {
                const karta = document.createElement("article");
                karta.className = "karta";
                const partner = document.createElement("p");
                partner.className = "partner";
                partner.textContent = oferta.partnerNazwa;
                const nazwa = document.createElement("h3");
                nazwa.textContent = oferta.nazwa;
                const opis = document.createElement("p");
                opis.className = "szczegoly";
                opis.textContent = oferta.opis;
                const cena = document.createElement("p");
                cena.className = "cena";
                cena.textContent = `${oferta.cena} zł`;
                const przycisk = document.createElement("button");
                przycisk.textContent = "Wybierz ofertę";
                przycisk.addEventListener("click", () => this.wybierzOferte(oferta));
                karta.append(partner, nazwa, opis, cena, przycisk);
                this.listaOfert.append(karta);
            });
    }

    wybierzOferte(oferta) {
        this.wybranaOferta = oferta;
        document.getElementById("nazwaWybranejOferty").textContent = `${oferta.nazwa} – ${oferta.cena} zł`;
        document.getElementById("zakup").hidden = false;
        document.getElementById("potwierdzenie").hidden = true;
        document.getElementById("zakup").scrollIntoView({ behavior: "smooth" });
        document.getElementById("emailKlienta").focus();
    }

    potwierdzZakup(zdarzenie) {
        zdarzenie.preventDefault();
        if (!this.wybranaOferta || !this.formularzZakupu.reportValidity()) return;
        this.numerZakupu += 1;
        const kontener = document.getElementById("kodyVoucherow");
        kontener.replaceChildren();
        for (let numerKodu = 1; numerKodu <= this.wybranaOferta.kody; numerKodu += 1) {
            const kod = document.createElement("p");
            kod.textContent = `DEMO-${String(this.numerZakupu).padStart(4, "0")}-${String(numerKodu).padStart(2, "0")}`;
            kontener.append(kod);
        }
        document.getElementById("zakup").hidden = true;
        document.getElementById("potwierdzenie").hidden = false;
        document.getElementById("potwierdzenie").scrollIntoView({ behavior: "smooth" });
    }

    wrocDoOfert() {
        this.wybranaOferta = null;
        this.formularzZakupu.reset();
        document.getElementById("zakup").hidden = true;
        document.getElementById("potwierdzenie").hidden = true;
        document.getElementById("oferty").scrollIntoView({ behavior: "smooth" });
    }
}

new SklepVoucherow();
