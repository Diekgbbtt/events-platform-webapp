

# New code for phase 3 - ChangeRequest code

def personalized_stats(request):
    user = current_user
    return render_template('personalized_stats.html', user=user)


def send_invite(request):
    user = Person.query.get(request.args["id"])
    event = Event.query.get(request.args["e"])
    invite = Invite()
    invite.event = event
    invite.invitedBy = current_user
    invite.invitee = user
    db.session.commit()
    return redirect(url_for('manage_event', id=request.args["e"]))


def accept_invitation(request):
    invite = Invite.query.get(request.args["id"])
    event = invite.event
    user = invite.invitee
    event.attendants.append(user)
    db.session.delete(invite)
    db.session.commit()
    return redirect(url_for('profile'))


def decline_invitation(request):
    invite = Invite.query.get(request.args["id"])
    db.session.delete(invite)
    db.session.commit()
    return redirect(url_for('profile'))
