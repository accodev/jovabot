# coding=utf-8
import telebot
import random
import time


jova_proverbs = ["Siete delle brutte persone",
                 "Siamo costellazioni di asteroidi su saturno che scambiano saluti col firmamento extracosmico",
                 "Ho votato Tsipras",
                 "Facciamoci un selfie",
                 "Guarda che ti tiro un sasso",
                 "Dio serpente",
                 "Salta chi può",
                 "San Benedetto la rondine sotto il tetto",
                 "San Lorenzo dalla gran calura.",
                 "San Silvestro  l'oliva nel canestro",
                 "Sangue giovane sempre spavaldo.",
                 "Sasso che rotola non fa muschio.",
                 "Pietra che rotola non fa muschio.",
                 "Sbagliando s'impara.",
                 "Scalda più l'amore che mille fuochi.",
                 "Scherza coi fanti e lascia stare i Santi.",
                 "Scherzando intorno al lume che t'invita, farfalla perderai l'ali e la vita.",
                 "Scherzo di mano, scherzo di villano.",
                 "Gioco di mano, gioco di villano.",
                 "Schiena di mulo, corso di barca, buon per chi n'accatta.",
                 "Scusa non richiesta, accusa manifesta.",
                 "Se ari male, peggio mieterai.",
                 "Se fossero buoni i nipoti non si leverebbero dalla vigna",
                 "Se gioventù sapesse, se vecchiaia potesse.",
                 "Se i gatti sapessero volare, le beccacce sarebbero rare.",
                 "Se il coltivatore non è più forte della su' terra questa finisce per divorarlo.",
                 "Se il poeta s'erige a oratore predicherà agli orecchi e non al cuore.",
                 "Se il tuo gatto è ladro non scacciarlo di casa.",
                 "Se il virtuoso è povero, il lodarlo non basta; il dovere primo è d'aiutarlo.",
                 "Se la pazzia fosse dolore, in ogni casa si sentirebbe stridere.",
                 "Se le lattughe lasci in guardia alle oche, al ritorno ne troverai ben poche.",
                 "Se nessuno sa quel che sai, a nulla serve il tuo sapere.",
                 "Se non è zuppa è pan bagnato.",
                 "Se occhio non mira, cuor non sospira.",
                 "Se piovesse oro, la gente si stancherebbe a raccoglierlo.",
                 "Se son rose fioriranno.",
                 "Se vuoi che t'ami, fa' che ti brami.",
                 "Senza denari non canta un cieco.",
                 "Senza denari non si canta messa.",
                 "Senza umiltà tutte le virtù sono vizi.",
                 "Sempre ti graffierà chi nacque gatto.",
                 "Senza umanità non vi è né virtù, né vero coraggio, né gloria durevole.",
                 "Sette in un colpo! disse quel sarto che aveva ammazzato sette mosche.",
                 "Si dice il peccato, ma non il peccatore.",
                 "Si può conoscere la tua opinione dal tuo sbadigliare",
                 "Si stava meglio quando si stava peggio.",
                 "Sol gente di mal'affare, bestie e botte, van fuori di notte.",
                 "Son padrone del mondo oggi le donne e cedon toghe e spade a cuffie e gonne.",
                 "Sono sempre gli stracci che vanno all'aria.",
                 "Sotto la neve pane, sotto l'acqua fame.",
                 "Spesso a chiaro mattino, v'è torbida sera.",
                 "Spesso vince più l'umiltà che il ferro.",
                 "Sposa bagnata sposa fortunata.",
                 "Stretta la foglia, larga la via dite la vostra che ho detto la mia.",
                 "Larga la foglia, stretta la via dite la vostra che ho detto la mia.",
                 "Studia non per sapere di più, ma per sapere meglio degli altri.",
                 "Sulla pelle della serpe nessuno guarda alle macchie.",
                 "Superbia povera spiace anche al diavolo; umiltà ricca piace anche a Dio."]

jova_solo = "Io lo fo che non fono folo\n" \
            "anche quando fono folo\n" \
            "io lo fo che non fono folo\n" \
            "e rido e piango e mi fondo con il cielo e con il fango"

jova_il_mondo = [ "Male.",
                  "Bene" ]


divinaCommedia = "In su l'estremità d'un'alta ripa\n" \
                 "che facevan gran pietre rotte in cerchio,\n" \
                 "venimmo sopra più crudele stipa;\n" \
                 "e quivi, per l'orribile soperchio\n" \
                 "del puzzo che 'l profondo abisso gitta,\n" \
                 "ci raccostammo, in dietro, ad un coperchio\n" \
                 "d'un grand' avello, ov' io vidi una scritta\n" \
                 "che dicea: 'Anastasio papa guardo, \n" \
                 "lo qual trasse Fotin de la via dritta'.\n" \
                 "«Lo nostro scender conviene esser tardo,\n" \
                 "sì che s'ausi un poco in prima il senso \n" \
                 "al tristo fiato; e poi no i fia riguardo».\n" \
                 "Così 'l maestro; e io «Alcun compenso», \n" \
                 "dissi lui, «trova che 'l tempo non passi \n" \
                 "perduto». Ed elli: «Vedi ch'a ciò penso».\n" \
                 "«Figliuol mio, dentro da cotesti sassi», \n" \
                 "cominciò poi a dir, «son tre cerchietti \n" \
                 "di grado in grado, come que' che lassi.\n" \
                 "Tutti son pien di spirti maladetti; \n" \
                 "ma perché poi ti basti pur la vista, \n" \
                 "intendi come e perché son costretti.\n" \
                 "D'ogne malizia, ch'odio in cielo acquista,\n" \
                 "ingiuria è 'l fine, ed ogne fin cotale \n" \
                 "o con forza o con frode altrui contrista.\n" \
                 "Ma perché frode è de l'uom proprio male,\n" \
                 "più spiace a Dio; e però stan di sotto \n" \
                 "li frodolenti, e più dolor li assale.\n" \
                 "Di vïolenti il primo cerchio è tutto;\n" \
                 "ma perché si fa forza a tre persone,\n" \
                 "in tre gironi è distinto e costrutto.\n" \
                 "A Dio, a sé, al prossimo si pòne\n" \
                 "far forza, dico in loro e in lor cose,\n" \
                 "come udirai con aperta ragione."

tb = None


def extract_token(filename):
    t = open(filename, "r")
    token = t.readline()
    print("token is %s" % token)
    return token


def listener(*messages):
    # When new messages arrive TeleBot will call this function.
    for m in messages:
        msg = m[0]  # dio can, coglione di telebot
        chat_id = msg.chat.id
        if msg.content_type == 'text':
            if 'jova' in msg.text.lower():
                if 'selfie' in msg.text.lower():
                    normal_msg = jova_proverbs[3].lower()
                elif 'proverbio' in msg.text.lower():
                    normal_msg = random.choice(jova_proverbs[6:]).lower()
                elif 'saluta' in msg.text.lower():
                    normal_msg = "Ti saluto {0}!".format(msg.from_user.first_name).lower()
                elif 'divina commedia' in msg.text.lower():
                    normal_msg = divinaCommedia.lower()
                elif 'sei solo' in msg.text.lower():
                    normal_msg = jova_solo.lower()
                elif 'come va il mondo' in msg.text.lower():
                    normal_msg = random.choice(jova_il_mondo).lower()
                else:
                    normal_msg = random.choice(jova_proverbs).lower()
                jova_msg = normal_msg.replace('s', 'f').replace('x', 'f')
                tb.send_chat_action(chat_id, 'typing')
                words_count = count_words(jova_msg)
                words_per_sec = 0.16
                time_to_write = words_count * words_per_sec
                print "word count {0} -> time to write {1} at {2} words per second".format(words_count, time_to_write,
                                                                                           words_per_sec)
                time.sleep(time_to_write)  # 33 wpm
                tb.send_message(chat_id, jova_msg)


def count_words(phrase):
    return len(phrase.split(" "))


def main():
    token = extract_token("key.token")
    global tb
    tb = telebot.TeleBot(token)
    tb.set_update_listener(listener)
    tb.polling()

    while True:
        pass


if __name__ == '__main__':
    main()